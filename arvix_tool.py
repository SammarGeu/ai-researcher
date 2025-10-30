# # Step1: Access arXiv using URL
# import requests


# def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
#     query = "+".join(topic.lower().split())
#     for char in list('()" '):
#         if char in query:
#             print(f"Invalid character '{char}' in query: {query}")
#             raise ValueError(f"Cannot have character: '{char}' in query: {query}")
#     url = (
#             "http://export.arxiv.org/api/query"
#             f"?search_query=all:{query}"
#             f"&max_results={max_results}"
#             "&sortBy=submittedDate"
#             "&sortOrder=descending"
#         )
#     print(f"Making request to arXiv API: {url}")
#     resp = requests.get(url)
    
#     if not resp.ok:
#         print(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
#         raise ValueError(f"Bad response from arXiv API: {resp}\n{resp.text}")
    
#     data = parse_arxiv_xml(resp.text)
#     return data


# # Step2: Parse XML
# import xml.etree.ElementTree as ET
# def parse_arxiv_xml(xml_content: str) -> dict:
#     """Parse the XML content from arXiv API response."""

#     entries = []
#     ns = {
#         "atom": "http://www.w3.org/2005/Atom",
#         "arxiv": "http://arxiv.org/schemas/atom"
#     }
#     root = ET.fromstring(xml_content)
#     # Loop through each <entry> in Atom namespace
#     for entry in root.findall("atom:entry", ns):
#         # Extract authors
#         authors = [
#             author.findtext("atom:name", namespaces=ns)
#             for author in entry.findall("atom:author", ns)
#         ]
        
#         # Extract categories (term attribute)
#         categories = [
#             cat.attrib.get("term")
#             for cat in entry.findall("atom:category", ns)
#         ]
        
#         # Extract PDF link (rel="related" and type="application/pdf")
#         pdf_link = None
#         for link in entry.findall("atom:link", ns):
#             if link.attrib.get("type") == "application/pdf":
#                 pdf_link = link.attrib.get("href")
#                 break

#         entries.append({
#             "title": entry.findtext("atom:title", namespaces=ns),
#             "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
#             "authors": authors,
#             "categories": categories,
#             "pdf": pdf_link
#         })

#     return {"entries": entries}



# # Step3: Convert the functionality into a tool
# #from langchain_core.tools import tool

# from langchain_core.tools import tool

# @tool
# def arxiv_search(topic: str) -> list[dict]:
#     """Search for recently uploaded arXiv papers

#     Args:
#         topic: The topic to search for papers about

#     Returns:
#         List of papers with their metadata including title, authors, summary, etc.
#     """
#     print("ARXIV Agent called")
#     print(f"Searching arXiv for papers about: {topic}")
#     papers = search_arxiv_papers(topic)
#     if len(papers) == 0:
#         print(f"No papers found for topic: {topic}")
#         raise ValueError(f"No papers found for topic: {topic}")
#     print(f"Found {len(papers['entries'])} papers about {topic}")
#     return papers


import requests
import xml.etree.ElementTree as ET
from langchain_core.tools import tool

def search_arxiv_papers(topic: str, max_results: int = 5) -> dict | str:
    """Internal function to search arXiv. Returns dict on success, str on error."""
    
    # --- THIS CHECK IS HARMFUL AND REMOVED ---
    # The requests library will handle URL encoding of spaces, '()', etc.
    # This check was blocking valid AI-generated queries.
    # for char in list('()" '):
    #     if char in query:
    #         print(f"Invalid character '{char}' in query: {query}")
    #         # --- BAD: This raises an error ---
    #         raise ValueError(f"Cannot have character: '{char}' in query: {query}")
    
    # The API can handle complex queries. We just replace spaces with '+'
    query = topic.lower().replace(" ", "+")
    
    url = (
            "http://export.arxiv.org/api/query"
            f"?search_query=all:{query}"
            f"&max_results={max_results}"
            "&sortBy=submittedDate"
            "&sortOrder=descending"
        )
    print(f"Making request to arXiv API: {url}")
    
    try:
        resp = requests.get(url, timeout=10) # Added a timeout
        resp.raise_for_status() # This will raise an HTTPError for bad responses (4xx, 5xx)
        
        data = parse_arxiv_xml(resp.text)
        
        if not data.get("entries"):
            # --- GOOD: Return error string ---
            return f"Error: No papers found on arXiv for the topic: '{topic}'"
            
        return data

    except requests.exceptions.RequestException as e:
        # --- GOOD: Return error string ---
        print(f"ArXiv API request failed: {e}")
        return f"Error: ArXiv API request failed. {str(e)}"
    except Exception as e:
        print(f"Error parsing arXiv XML: {e}")
        return f"Error: Failed to parse arXiv XML response. {str(e)}"


def parse_arxiv_xml(xml_content: str) -> dict:
    """Parse the XML content from arXiv API response."""
    # ... (Your XML parsing logic is excellent and unchanged) ...
    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_content)
    for entry in root.findall("atom:entry", ns):
        authors = [
            author.findtext("atom:name", namespaces=ns)
            for author in entry.findall("atom:author", ns)
        ]
        categories = [
            cat.attrib.get("term")
            for cat in entry.findall("atom:category", ns)
        ]
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break
        entries.append({
            "title": entry.findtext("atom:title", namespaces=ns),
            "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
            "authors": authors,
            "categories": categories,
            "pdf": pdf_link
        })
    return {"entries": entries}


@tool
def arxiv_search(topic: str) -> dict | str:
    """Search for recently uploaded arXiv papers.
    On success, returns a list of papers.
    On failure, returns an error message string.

    Args:
        topic: The topic to search for papers about

    Returns:
        List of papers with their metadata OR an error string.
    """
    print("ARXIV Agent called")
    print(f"Searching arXiv for papers about: {topic}")
    
    papers_or_error = search_arxiv_papers(topic)
    
    if isinstance(papers_or_error, str):
        # It's an error string, just return it
        print(papers_or_error)
        return papers_or_error

    print(f"Found {len(papers_or_error['entries'])} papers about {topic}")
    return papers_or_error
