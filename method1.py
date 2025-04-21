import csv
import re
import requests
import json
import time

# 修改API密钥
TAVILY_API_KEY = "Sorry but we cannot show this"
DEEPSEEK_API_KEY = "and this"

def search_tavily(query: str, search_depth: str = "advanced", max_results: int = 5):
    """
    使用 Tavily API 进行网络搜索
    """
    try:
        url = "https://api.tavily.com/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TAVILY_API_KEY}"
        }
        data = {
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"搜索错误: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"搜索时发生错误: {str(e)}")
        return []

def query_deepseek(prompt: str, search_results: list):
    """
    使用 DeepSeek 模型分析搜索结果
    """
    try:
        # 构建包含搜索结果的提示
        context = "基于以下搜索结果，请回答用户的问题。\n\n"
        context += f"用户问题: {prompt}\n\n"
        context += "搜索结果:\n"
        
        for i, result in enumerate(search_results, 1):
            context += f"{i}. {result['title']}\n"
            context += f"   URL: {result['url']}\n"
            context += f"   描述: {result['content']}\n\n"
        
        context += "请基于上述搜索结果，提供一个全面、准确的回答。"
        
        # 调用 DeepSeek API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个基于实时网络搜索结果的AI助手,请提供准确、全面的回答。"},
                {"role": "user", "content": context}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"DeepSeek API 请求失败: {response.status_code}")
            return "无法获取回答。"
            
    except Exception as e:
        print(f"DeepSeek 查询时发生错误: {str(e)}")
        return "处理请求时发生错误。"

def extract_contact_info(text):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phones = re.findall(r'\+?[\d\s-]{8,}', text)
    
    contact_info = []
    if emails:
        contact_info.extend(emails)
    if phones:
        contact_info.extend(phones)
    
    return ','.join(contact_info)

def process_university(university_name):
    query = f"{university_name} Duolingo English Test acceptance language requirements"
    search_results = search_tavily(query, search_depth="advanced", max_results=5)
    
    if not search_results:
        return "not mentioned", "", "", "", ""
    
    # 使用DeepSeek分析结果
    analysis_prompt = f"""基于以下搜索结果，判断{university_name}是否接受多邻国英语测试作为入学语言要求。
请只回答以下四种情况之一：
1. accepted - 明确接受多邻国考试
2. partially accepted - 部分接受或特定条件下接受
3. not accepted - 明确不接受
4. not mentioned - 未提及或无法确定

同时请提供：
1. 信息来源URL
2. 接受的项目（Undergraduate/Graduate/PhD/others，可以多选，用逗号分隔）
3. 学校的联系方式（如招生办公室邮箱或电话）"""

    result_text = query_deepseek(analysis_prompt, search_results)
    
    # 解析结果
    result_text = result_text.lower()
    if "accepted" in result_text:
        status = "accepted"
    elif "partially accepted" in result_text:
        status = "partially accepted"
    elif "not accepted" in result_text:
        status = "not accepted"
    else:
        status = "not mentioned"
    
    source = ""
    if status != "not mentioned": 
        for result in search_results:
            if result.get('url'):
                source = result['url']
                break
    
    programs = ""
    if status != "not mentioned":
        if "undergraduate" in result_text:
            programs += "Undergraduate,"
        if "graduate" in result_text or "master" in result_text:
            programs += "Graduate,"
        if "phd" in result_text or "doctoral" in result_text:
            programs += "PhD,"
        if "diploma" in result_text or "certificate" in result_text or "foundation" in result_text:
            programs += "others,"
        programs = programs.rstrip(",")
    
    contact = ""
    contact_source = ""
    if status != "not mentioned":
        contact_query = f"{university_name} admissions contact email phone"
        contact_results = search_tavily(contact_query, search_depth="basic", max_results=3)
        if contact_results:
            contact = extract_contact_info(contact_results[0].get('content', ''))
            contact_source = contact_results[0].get('url', '')
    
    return status, source, programs, contact, contact_source

def main():
    # 修改输入文件路径
    with open('data_to_import.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        universities = list(reader)
    
    # 处理每所大学
    results = []
    for uni in universities[890:1000]: # 处理500-1000所
        print(f"Processing {uni['name']}...")
        status, source, programs, contact, contact_source = process_university(uni['name'])
        
        result = {
            'name': uni['name'],
            'domains': uni['domains'],
            'web_pages': uni['web_pages'],
            'location_id': uni['location_id'],
            'duolingo_acceptance': status,
            'source': source,
            'programs': programs,
            'contact': contact,
            'contact_source': contact_source
        }
        results.append(result)
        
        # 每处理10所学校保存一次结果
        if len(results) % 10 == 0:
            with open('duolingo_acceptance.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'domains', 'web_pages', 'location_id', 'duolingo_acceptance', 'source', 'programs', 'contact', 'contact_source'])
                writer.writeheader()
                writer.writerows(results)
            print(f"已保存 {len(results)} 所学校的结果")
    
    # 最后保存所有结果
    with open('duolingo_acceptance.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'domains', 'web_pages', 'location_id', 'duolingo_acceptance', 'source', 'programs', 'contact', 'contact_source'])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main() 