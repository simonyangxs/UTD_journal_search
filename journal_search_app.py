import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
from datetime import datetime
import json
import time
# streamlit run journal_search_app.py
# 设置页面配置
st.set_page_config(
    page_title="Business Journal Search Tool",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加CSS样式固定侧边栏宽度
st.markdown("""
<style>
    .css-1d391kg {
        width: 420px !important;
        min-width: 420px !important;
        max-width: 420px !important;
    }
    
    .css-1lcbmhc {
        width: 420px !important;
        min-width: 420px !important;
        max-width: 420px !important;
    }
    
    section[data-testid="stSidebar"] {
        width: 420px !important;
        min-width: 420px !important;
        max-width: 420px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        width: 420px !important;
        min-width: 420px !important;
        max-width: 420px !important;
    }
</style>
""", unsafe_allow_html=True)

UTD_24_JOURNALS = [
    # OM
    "Journal of Operations Management (JOM)",
    "Manufacturing & Service Operations Management (MSOM)",
    "Operations Research (OR)",
    "Production and Operations Management (POMS)",
    "Organization Science (OS)",
    
    # Finance
    "Journal of Finance (JF)",
    "Journal of Financial Economics (JFE)",
    "Review of Financial Studies (RFS)",
    
    # Accounting
    "The Accounting Review (AR)",
    "Journal of Accounting and Economics (JAE)",
    "Journal of Accounting Research (JAR)",
    "Journal of International Business Studies (JIBS)",
    
    # Management
    "Academy of Management Journal (AMJ)",
    "Academy of Management Review (AMR)",
    "Administrative Science Quarterly (ASQ)",
    "Management Science (MS)",
    "Strategic Management Journal (SMJ)",
    
    # Marketing
    "Journal of Consumer Research (JCR)",
    "Journal of Marketing (JM)",
    "Journal of Marketing Research (JMR)",
    "Marketing Science (MS)",
    
    # Information Systems
    "Information Systems Research (ISR)",
    "MIS Quarterly (MISQ)",
    "Journal on Computing (JC)"

]

# 定义FT50期刊列表 (从当前可用期刊中选择)
FT50_JOURNALS = [
    # Economics
    "American Economic Review (AER)",
    "Econometrica",
    "Journal of Political Economy (JPE)", 
    "Quarterly Journal of Economics (QJE)",
    "Review of Economic Studies (RES)",
    "Journal of International Economics (JIE)",
    
    # Finance
    "Journal of Finance (JF)",
    "Journal of Financial Economics (JFE)",
    "Journal of Financial and Quantitative Analysis (JFQA)",
    "Review of Financial Studies (RFS)",
    "Review of Finance (RF)",
    
    # Accounting
    "The Accounting Review (AR)",
    "Accounting, Organizations and Society (AOS)",
    "Contemporary Accounting Research (CAR)",
    "Journal of Accounting and Economics (JAE)",
    "Journal of Accounting Research (JAR)",
    "Review of Accounting Studies (RAS)",
    
    # Management
    "Academy of Management Journal (AMJ)",
    "Academy of Management Review (AMR)",
    "Administrative Science Quarterly (ASQ)",
    "Journal of Management (JM)",
    "Journal of Management Studies (JMS)",
    "Management Science (MS)",
    "Organization Science (OS)",
    "Strategic Management Journal (SMJ)",
    "Human Relations (HR)",
    "Human Resource Management (HRM)",
    "Entrepreneurship Theory and Practice (ETP)",
    "Journal of Business Venturing (JBV)",
    "Journal of Business Ethics (JBE)",
    "Strategic Entrepreneurship Journal (SEJ)",
    
    # Marketing
    "Journal of Consumer Research (JCR)",
    "Journal of Marketing (JM)",
    "Journal of Marketing Research (JMR)",
    "Marketing Science (MS)",
    "Journal of Consumer Psychology (JCP)",
    "Journal of the Academy of Marketing Science (JAMS)",
    
    # Information Systems
    "Information Systems Research (ISR)",
    "MIS Quarterly (MISQ)",
    "Journal of Management Information Systems (JMIS)",
    
    # Operations
    "Journal of Operations Management (JOM)",
    "Manufacturing & Service Operations Management (MSOM)",
    "Operations Research (OR)",
    "Production and Operations Management (POMS)",
    
    # Others
    "Journal of International Business Studies (JIBS)",
    "Research Policy (RP)",
    "Organization Studies (OS)",
    "Organizational Behavior and Human Decision Processes (OBHDP)"
]

# 定义期刊搜索链接配置
JOURNAL_CONFIGS = {
    # INFORMS 期刊
    "Management Science (MS)": {
        "base_url": "https://pubsonline.informs.org/action/doSearch",
        "params": {
            "field1": "AllField",
            "text1": "",
            "publication[]": ["mnsc"],
            "publication": "",
            "BeforeYear": "",
            "BeforeMonth": "",
            "AfterMonth": "",
            "AfterYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Manufacturing & Service Operations Management (MSOM)": {
        "base_url": "https://pubsonline.informs.org/action/doSearch",
        "params": {
            "field1": "AllField",
            "text1": "",
            "publication[]": ["msom"],
            "publication": "",
            "BeforeYear": "",
            "BeforeMonth": "",
            "AfterMonth": "",
            "AfterYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Information Systems Research (ISR)": {
        "base_url": "https://pubsonline.informs.org/action/doSearch",
        "params": {
            "field1": "AllField",
            "text1": "",
            "publication[]": ["isre"],
            "publication": "",
            "BeforeYear": "",
            "BeforeMonth": "",
            "AfterMonth": "",
            "AfterYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Organization Science (OS)": {
        "base_url": "https://pubsonline.informs.org/action/doSearch",
        "params": {
            "field1": "AllField",
            "text1": "",
            "publication[]": ["orsc"],
            "publication": "",
            "BeforeYear": "",
            "BeforeMonth": "",
            "AfterMonth": "",
            "AfterYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Marketing Science (MS)": {
        "base_url": "https://pubsonline.informs.org/action/doSearch",
        "params": {
            "field1": "AllField",
            "text1": "",
            "publication[]": ["mksc"],
            "publication": "",
            "BeforeYear": "",
            "BeforeMonth": "",
            "AfterMonth": "",
            "AfterYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Operations Research (OR)": {
        "base_url": "https://pubsonline.informs.org/action/doSearch",
        "params": {
            "field1": "AllField",
            "text1": "",
            "publication[]": ["opre"],
            "publication": "",
            "BeforeYear": "",
            "BeforeMonth": "",
            "AfterMonth": "",
            "AfterYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Journal on Computing (JC)": {
        "base_url": "https://pubsonline.informs.org/action/doSearch",
        "params": {
            "field1": "AllField",
            "text1": "",
            "publication[]": ["ijoc"],
            "publication": "",
            "BeforeYear": "",
            "BeforeMonth": "",
            "AfterMonth": "",
            "AfterYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },

    # ScienceDirect 期刊
    "Journal of International Economics (JIE)": {
        "base_url": "https://www.sciencedirect.com/search",
        "params": {
            "qs": "",
            "title": "",
            "tak":"",
            "publicationTitles": "271695",
            "lastSelectedFacet": "years",
            "years": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Journal of Accounting and Economics (JAE)": {
        "base_url": "https://www.sciencedirect.com/search",
        "params": {
            "qs": "",
            "title": "",
            "tak":"",
            "publicationTitles": "271671",
            "lastSelectedFacet": "years",
            "years": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Journal of Financial Economics (JFE)": {
        "base_url": "https://www.sciencedirect.com/search",
        "params": {
            "qs": "",
            "title": "",
            "tak":"",
            "publicationTitles": "271661",
            "lastSelectedFacet": "years",
            "years": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Accounting, Organizations and Society (AOS)": {
        "base_url": "https://www.sciencedirect.com/search",
        "params": {
            "qs": "",
            "title": "",
            "tak":"",
            "publicationTitles": "271665",
            "lastSelectedFacet": "years",
            "years": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Journal of Business Venturing (JBV)": {
        "base_url": "https://www.sciencedirect.com/search",
        "params": {
            "qs": "",
            "title": "",
            "tak":"",
            "publicationTitles": "271663",
            "lastSelectedFacet": "years",
            "years": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Organizational Behavior and Human Decision Processes (OBHDP)": {
        "base_url": "https://www.sciencedirect.com/search",
        "params": {
            "qs": "",
            "title": "",
            "tak":"",
            "publicationTitles": "272419",
            "lastSelectedFacet": "years",
            "years": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Research Policy (RP)": {
        "base_url": "https://www.sciencedirect.com/search",
        "params": {
            "qs": "",
            "title": "",
            "tak":"",
            "publicationTitles": "271666",
            "lastSelectedFacet": "years",
            "years": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    
    # MISQ
    "MIS Quarterly (MISQ)": {
        "base_url": "https://misq.umn.edu/catalogsearch/advanced/result/",
        "params": {
            "name": "",
            "description": "",
            "misq_year[from]": "",
            "misq_year[to]": "",
            "misq_author": "",
            "misq_volume": "",
            "misq_issue": ""
        },
        "search_fields": ["Title", "Abstract"],
        "supports_date": True
    },
    
    # AEA
    "American Economic Review (AER)": {
        "base_url": "https://www.aeaweb.org/journals/aer/search-results",
        "params": {
            "ArticleSearch[within][articletitle]": "",
            "ArticleSearch[within][articleabstract]": "",
            "ArticleSearch[within][authorlast]": "0",
            "JelClass[value]": "0",
            "journal": "1",
            "ArticleSearch[q]": ""
        },
        "search_fields": ["Title", "Abstract"],
        "supports_date": False
    },
    
    # Oxford 期刊
    "Quarterly Journal of Economics (QJE)": {
        "base_url": "https://academic.oup.com/journals/search-results",
        "params": {
            "allJournals": "1",
            "f_JournalID": "3365",
            "fl_SiteID": "5567",
            "rg_ArticleDate": "",
            "dateFilterType": "",
            "noDateTypes": "",
            "rg_AllPublicationDates": "",
            "rg_VersionDate": "",
            "cqb": "",
            "qb": "",
            "page": "1"
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Review of Financial Studies (RFS)": {
        "base_url": "https://academic.oup.com/journals/search-results",
        "params": {
            "allJournals": "1",
            "f_JournalID": "3372",
            "fl_SiteID": "5567",
            "rg_ArticleDate": "",
            "dateFilterType": "",
            "noDateTypes": "",
            "rg_AllPublicationDates": "",
            "rg_VersionDate": "",
            "cqb": "",
            "qb": "",
            "page": "1"
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Review of Economic Studies (RES)": {
        "base_url": "https://academic.oup.com/journals/search-results",
        "params": {
            "allJournals": "1",
            "f_JournalID": "3369",
            "fl_SiteID": "5567",
            "rg_ArticleDate": "",
            "dateFilterType": "",
            "noDateTypes": "",
            "rg_AllPublicationDates": "",
            "rg_VersionDate": "",
            "cqb": "",
            "qb": "",
            "page": "1"
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Journal of Consumer Research (JCR)": {
        "base_url": "https://academic.oup.com/journals/search-results",
        "params": {
            "allJournals": "1",
            "f_JournalID": "3258",
            "fl_SiteID": "5567",
            "rg_ArticleDate": "",
            "dateFilterType": "",
            "noDateTypes": "",
            "rg_AllPublicationDates": "",
            "rg_VersionDate": "",
            "cqb": "",
            "qb": "",
            "page": "1"
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Review of Finance (RF)": {
        "base_url": "https://academic.oup.com/journals/search-results",
        "params": {
            "allJournals": "1",
            "f_JournalID": "3371",
            "fl_SiteID": "5567",
            "rg_ArticleDate": "",
            "dateFilterType": "",
            "noDateTypes": "",
            "rg_AllPublicationDates": "",
            "rg_VersionDate": "",
            "cqb": "",
            "qb": "",
            "page": "1"
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    
    # Wiley 期刊
    "Journal of Finance (JF)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["15406261"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Journal of Accounting Research (JAR)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["1475679x"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Strategic Management Journal (SMJ)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["10970266"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Contemporary Accounting Research (CAR)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["19113846"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Journal of Consumer Psychology (JCP)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["15327663"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Journal of Management Studies (JMS)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["14676486"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Econometrica": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["14680262"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Human Resource Management (HRM)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["1099050x"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Strategic Entrepreneurship Journal (SEJ)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["1932443x"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Journal of Operations Management (JOM)": {
        "base_url": "https://onlinelibrary.wiley.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["18731317"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    
    # Chicago
    "Journal of Political Economy (JPE)": {
        "base_url": "https://www.journals.uchicago.edu/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["jpe"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField"],
        "supports_date": True
    },
    
    # Sage 期刊
    "Administrative Science Quarterly (ASQ)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["asqa"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Entrepreneurship Theory and Practice (ETP)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["etpb"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Human Relations (HR)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["huma"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Journal of Management (JM)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["joma"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    }, 
    "Organization Studies (OS)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["ossa"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    }, 
    "Production and Operations Management (POMS)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["paoa"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    "Journal of Marketing (JM)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["jmxa"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    }, 
    "Journal of Marketing Research (JMR)": {
        "base_url": "https://journals.sagepub.com/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["mrj"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": "",
            "access": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },
    
    # AAA
    "The Accounting Review (AR)": {
        "base_url": "https://publications.aaahq.org/search-results",
        "params": {
            "q": "",
            "f_JournalDisplayName": "The+Accounting+Review",
            "fl_JournalID": "1000017",
            "fl_SiteID": "1",
            "rg_PublicationDate": "",
            "qb": "",
            "page": "1"
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True,
        "special_format": {
            "Abstract": "Abstract1",
            "Title": "Title1", 
            "AllField": "AllField1"
        }
    },
    
    # springer： 搜索出来的journal合并使用 OR 即可
    "Journal of International Business Studies (JIBS)": {
            "base_url": "https://link.springer.com/search",
            "params": {
                "new-search": "true",
                "advancedSearch": "true", 
                "sortBy": "relevance",
                "query": "",
                "title": "",
                "contributor": "",
                "journal": "Journal of International Business Studies",
                "date": "custom",
                "dateFrom": "",
                "dateTo": ""
            },
            "search_fields": ["AllField", "Title"],
            "supports_date": True
    },
    "Journal of Business Ethics (JBE)": {
        "base_url": "https://link.springer.com/search",
        "params": {
            "new-search": "true",
            "advancedSearch": "true", 
            "sortBy": "relevance",
            "query": "",
            "title": "",
            "contributor": "",
            "journal": "Journal of Business Ethics",
            "date": "custom",
            "dateFrom": "",
            "dateTo": ""
        },
        "search_fields": ["AllField", "Title"],
        "supports_date": True
    },
    "Review of Accounting Studies (RAS)": {
        "base_url": "https://link.springer.com/search",
        "params": {
            "new-search": "true",
            "advancedSearch": "true", 
            "sortBy": "relevance",
            "query": "",
            "title": "",
            "contributor": "",
            "journal": "Review of Accounting Studies",
            "date": "custom",
            "dateFrom": "",
            "dateTo": ""
        },
        "search_fields": ["AllField", "Title"],
        "supports_date": True
    },
    "Journal of the Academy of Marketing Science (JAMS)": {
        "base_url": "https://link.springer.com/search",
        "params": {
            "new-search": "true",
            "advancedSearch": "true", 
            "sortBy": "relevance",
            "query": "",
            "title": "",
            "contributor": "",
            "journal": "Journal of the Academy of Marketing Science",
            "date": "custom",
            "dateFrom": "",
            "dateTo": ""
        },
        "search_fields": ["AllField", "Title"],
        "supports_date": True
    },

    #cambridge
    "Journal of Financial and Quantitative Analysis (JFQA)": {
        "base_url": "https://www.cambridge.org/core/search",
        "params": {
            "q": "",
            "aggs[productJournal][filters]": "FB35548FF614F4556E96D01FA2CB412E",
            "filters[dateYearRange][from]": "",
            "filters[dateYearRange][to]": "",
            "fts": "", #全文就是yes，title就是no
        },
        "search_fields": ['Title'],
        "supports_date": True
    },

    # Taylor & Francis
    "Journal of Management Information Systems (JMIS)": {
        "base_url": "https://www.tandfonline.com/action/doSearch",
        "params": {
            "field1": "",
            "text1": "",
            "SeriesKey": "mmis20",
            "AfterYear": "",
            "BeforeYear": ""
        },
        "search_fields": ["AllField", "Title", "Abstract"],
        "supports_date": True
    },

    # AOM
    "Academy of Management Journal (AMJ)": {
        "base_url": "https://journals.aom.org/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["amj"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    "Academy of Management Review (AMR)": {
        "base_url": "https://journals.aom.org/action/doSearch",
        "params": {
            "field1": "Title",
            "text1": "",
            "publication[]": ["amr"],
            "publication": "",
            "Ppub": "",
            "AfterMonth": "",
            "AfterYear": "",
            "BeforeMonth": "",
            "BeforeYear": ""
        },
        "search_fields": ["Title", "AllField", "Abstract"],
        "supports_date": True
    },
    
    # NBER Working Papers
    "NBER": {
        "base_url": "https://www.nber.org/search",
        "params": {
            "q": "",
            "startDate": "",
            "endDate": "",
            "facet": "contentType:working_paper",
            "page": "1",
            "perPage": "50"
        },
        "search_fields": ["AllField"],
        "supports_date": True
    }
}

def update_journal_selection(journal):
    """更新期刊选择状态的回调函数"""
    checkbox_key = f"{journal}"
    if st.session_state.get(checkbox_key, False):  # 如果复选框被选中
        if journal not in st.session_state.selected_journals:
            st.session_state.selected_journals.append(journal)
    else:  # 如果复选框未被选中
        if journal in st.session_state.selected_journals:
            st.session_state.selected_journals.remove(journal)

def group_journals_by_website(selected_journals):
    """按网站对期刊进行分组"""
    website_groups = {}
    
    for journal in selected_journals:
        if journal not in JOURNAL_CONFIGS:
            continue
            
        base_url = JOURNAL_CONFIGS[journal]['base_url']
        website = base_url.split('/')[2]  # 提取域名
        
        if website not in website_groups:
            website_groups[website] = []
        website_groups[website].append(journal)
        
    return website_groups

def generate_combined_search_url(journals, search_term, search_field, start_year, end_year,
                               start_month=None, end_month=None):
    """为同一网站的期刊生成搜索URL，支持单个或多个期刊，支持年月范围"""
    if not journals:
        return None
        
    # 使用第一个期刊作为模板
    template_journal = journals[0]
    config = JOURNAL_CONFIGS[template_journal]
    base_url = config['base_url']
    params = config['params'].copy()
    website = base_url.split('/')[2]
    
    # 检查是否支持日期筛选
    supports_date = config.get('supports_date', False)
    if not supports_date:
        start_year = end_year = start_month = end_month = None
    
    # 根据网站类型处理参数
    if 'informs.org' in website:
        # INFORMS 期刊 - 支持日期和月份筛选
        if len(journals) > 1:
            # 多个期刊合并
            publications = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    pub_list = JOURNAL_CONFIGS[journal]['params'].get('publication[]', [])
                    publications.extend(pub_list)
            params['publication[]'] = publications
        # 单个期刊直接使用模板配置中的 publication[]
        
        params['text1'] = search_term
        if search_field == "Title":
            params['field1'] = "Title"
        elif search_field == "Abstract":
            params['field1'] = "Abstract"
        else:
            params['field1'] = "AllField"
        # 添加日期和月份筛选支持
        if start_year and end_year:
            params['AfterYear'] = start_year
            params['BeforeYear'] = end_year
            params['AfterMonth'] = str(start_month) if start_month else "1"
            params['BeforeMonth'] = str(end_month) if end_month else "12"
            
    elif 'sciencedirect.com' in website:
        # ScienceDirect 期刊 - 支持不同搜索字段
        if len(journals) > 1:
            # 多个期刊合并
            publication_titles = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    pub_titles = JOURNAL_CONFIGS[journal]['params'].get('publicationTitles', '')
                    if pub_titles:
                        publication_titles.append(pub_titles)
            params['publicationTitles'] = ','.join(publication_titles)
        
        # 根据搜索字段设置参数
        if search_field == "Title":
            params['title'] = search_term
            # 清空qs参数
            if 'qs' in params:
                del params['qs']
            if 'tak' in params:
                del params['tak']
        elif search_field == "Abstract":
            params['tak'] = search_term
            # 清空title参数
            if 'title' in params:
                del params['title']
            if 'qs' in params:
                del params['qs']
        else:  
            params['qs'] = search_term
            # 清空title参数
            if 'title' in params:
                del params['title']
            if 'tak' in params:
                del params['tak']
                
        if start_year and end_year:
            years = ",".join([str(y) for y in range(int(start_year), int(end_year)+1)])
            params['years'] = years
            
    elif template_journal == "MIS Quarterly (MISQ)":
        # MISQ 特殊处理
        if search_field == "Title":
            params["name"] = f'"{search_term}"'
        elif search_field == "Abstract":
            params["description"] = search_term
        if start_year:
            params["misq_year[from]"] = start_year
        if end_year:
            params["misq_year[to]"] = end_year
            
    elif template_journal == "American Economic Review (AER)":
        # AER 特殊处理
        clean_search_term = search_term.replace('"', '').replace("'", "").replace(""", "").replace(""", "")
        params["ArticleSearch[q]"] = clean_search_term
        
        # 根据搜索字段设置相应的搜索范围
        if search_field == "Title":
            params["ArticleSearch[within][articletitle]"] = "1"
            params["ArticleSearch[within][articleabstract]"] = "0"
        elif search_field == "Abstract":
            params["ArticleSearch[within][articletitle]"] = "0"
            params["ArticleSearch[within][articleabstract]"] = "1"
        else:
            params["ArticleSearch[within][articletitle]"] = "1"
            params["ArticleSearch[within][articleabstract]"] = "1"
            
    elif 'oup.com' in website:
        # Oxford 期刊 - 支持年月筛选和不同搜索字段
        if len(journals) > 1:
            # 多个期刊合并
            journal_ids = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    j_id = JOURNAL_CONFIGS[journal]['params'].get('f_JournalID', '')
                    if j_id:
                        journal_ids.append(j_id)
            params['f_JournalID'] = 'AND'.join(journal_ids)
        # 单个期刊直接使用模板配置中的 f_JournalID
        
        if start_year and end_year:
            # 默认使用月份的第一天和最后一天
            start_date = f"{start_month:02d}%2f01%2f{start_year}" if start_month else f"01%2f01%2f{start_year}"
            
            # 计算结束月份的最后一天
            if end_month:
                if end_month in [1, 3, 5, 7, 8, 10, 12]:
                    last_day = 31
                elif end_month in [4, 6, 9, 11]:
                    last_day = 30
                else:  # 2月
                    # 简单处理闰年，2月按28天算
                    last_day = 28
                end_date = f"{end_month:02d}%2f{last_day:02d}%2f{end_year}"
            else:
                end_date = f"12%2f31%2f{end_year}"
                
            date_range = f"{start_date}+TO+{end_date}"
            params['rg_ArticleDate'] = date_range
            params['dateFilterType'] = "range"
            params['noDateTypes'] = "true"
            params['rg_AllPublicationDates'] = date_range
            params['rg_VersionDate'] = date_range
        
        # 根据搜索字段设置不同的filter和qb参数
        clean_search_term = search_term.replace('"', '').replace("'", "").replace(""", "").replace(""", "")

        if search_field == "Title":
            params['cqb'] = f'[{{"terms":[{{"filter":"Title","input":"{clean_search_term}","exactMatch":true}}]}}]'
            params['qb'] = f'{{"Title1-exact":"{clean_search_term}"}}'
        elif search_field == "Abstract":
            params['cqb'] = f'[{{"terms":[{{"filter":"ContentAbstract","input":"{clean_search_term}","exactMatch":true}}]}}]'
            params['qb'] = f'{{"ContentAbstract1-exact":"{clean_search_term}"}}'
        else:  
            params['cqb'] = f'[{{"terms":[{{"filter":"_text_","input":"{clean_search_term}","exactMatch":true}}]}}]'
            params['qb'] = f'{{"_text_1-exact":"{clean_search_term}"}}'
        
    elif 'wiley.com' in website:
        # Wiley 期刊 - 支持月份筛选
        if len(journals) > 1:
            # 多个期刊合并
            publications = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    pub_list = JOURNAL_CONFIGS[journal]['params'].get('publication[]', [])
                    publications.extend(pub_list)
            params['publication[]'] = publications
        # 单个期刊直接使用模板配置中的 publication[]
        
        params['text1'] = search_term.replace(" ", "+")
        if search_field == "Title":
            params['field1'] = "Title"
        elif search_field == "AllField":
            params['field1'] = "AllField"
        elif search_field == "Abstract":
            params['field1'] = "Abstract"
        else:
            params['field1'] = "AllField"
            
        if start_year and end_year:
            params['AfterYear'] = start_year
            params['BeforeYear'] = end_year
            params['AfterMonth'] = str(start_month) if start_month else "1"
            params['BeforeMonth'] = str(end_month) if end_month else "12"
            
    elif 'journals.uchicago.edu' in website:
        # Chicago 期刊 (JPE) - 支持月份筛选
        params['text1'] = search_term  # JPE不需要+号替换
        if search_field == "Title":
            params['field1'] = "Title"
        else:
            params['field1'] = "AllField"
            
        if start_year and end_year:
            params['AfterYear'] = start_year
            params['BeforeYear'] = end_year
            params['AfterMonth'] = str(start_month) if start_month else "1"
            params['BeforeMonth'] = str(end_month) if end_month else "12"
            
    elif 'sagepub.com' in website:
        # Sage 期刊 - 支持月份筛选
        if len(journals) > 1:
            # 多个期刊合并
            publications = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    pub_list = JOURNAL_CONFIGS[journal]['params'].get('publication[]', [])
                    publications.extend(pub_list)
            params['publication[]'] = publications
        # 单个期刊直接使用模板配置中的 publication[]
        
        params['text1'] = search_term
        # 根据搜索字段设置field1参数
        if search_field == "Title":
            params['field1'] = "Title"
        elif search_field == "AllField":
            params['field1'] = "AllField" 
        elif search_field == "Abstract":
            params['field1'] = "Abstract"
        else:
            params['field1'] = "AllField"
            
        if start_year and end_year:
            params['AfterYear'] = start_year
            params['BeforeYear'] = end_year
            params['AfterMonth'] = str(start_month) if start_month else "1"
            params['BeforeMonth'] = str(end_month) if end_month else "12"
            
    elif 'publications.aaahq.org' in website:
        # AAA 期刊 (AR) - 支持精确日期筛选和特殊搜索格式
        config = JOURNAL_CONFIGS[template_journal]
        special_format = config.get("special_format", {})
        
        # 对搜索词中的引号进行转义
        escaped_search_term = search_term.replace('"', '\\"').replace("'", "\\'") #.replace("“", "\\“").replace("”", "\\”")
        
        # 根据搜索字段设置特殊格式的qb参数
        if search_field == "Title":
            field_name = special_format.get("Title", "Title1")
            params["qb"] = f'{{"{field_name}":"{escaped_search_term}"}}'
        elif search_field == "Abstract":
            field_name = special_format.get("Abstract", "Abstract1")
            params["qb"] = f'{{"{field_name}":"{escaped_search_term}"}}'
        else: 
            field_name = special_format.get("Anywhere", "Abstract1")
            params["qb"] = f'{{"{field_name}":"{escaped_search_term}"}}'
        
        # 清空q参数，使用qb参数进行搜索
        if "q" in params:
            params["q"] = ""
            
        if start_year and end_year:
            # 使用年月范围，默认使用月份的第一天和最后一天
            start_date = f"{start_year}-{start_month:02d}-01" if start_month else f"{start_year}-01-01"
            
            # 计算结束月份的最后一天
            if end_month:
                if end_month in [1, 3, 5, 7, 8, 10, 12]:
                    last_day = 31
                elif end_month in [4, 6, 9, 11]:
                    last_day = 30
                else:  # 2月
                    # 简单处理闰年，2月按28天算
                    last_day = 28
                end_date = f"{end_year}-{end_month:02d}-{last_day:02d}"
            else:
                end_date = f"{end_year}-12-31"
                
            date_range = f"{start_date}T00:00:00 TO {end_date}T23:59:59"
            params["rg_PublicationDate"] = date_range
            
    elif 'journals.aom.org' in website:
        # AOM 期刊 (AMJ/AMR) - 支持月份筛选和多期刊合并
        if len(journals) > 1:
            # 多个期刊合并
            publications = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    pub_list = JOURNAL_CONFIGS[journal]['params'].get('publication[]', [])
                    publications.extend(pub_list)
            params['publication[]'] = publications
        # 单个期刊直接使用模板配置中的 publication[]
        
        search_term = search_term.replace(""", '"').replace(""", '"')
        params['text1'] = search_term.replace(" ", "+")
        if search_field == "Title":
            params['field1'] = "Title"
        elif search_field == "Abstract":
            params['field1'] = "Abstract"
        else:
            params['field1'] = "AllField"
            
        if start_year and end_year:
            params['AfterYear'] = start_year
            params['BeforeYear'] = end_year
            params['AfterMonth'] = str(start_month) if start_month else "1"
            params['BeforeMonth'] = str(end_month) if end_month else "12"
    elif 'cambridge.org' in website:
        # Cambridge 期刊 - 支持年份筛选
        params['q'] = search_term

        if search_field == "Title":
            params['fts'] = "no"
        else:
            params['fts'] = "yes"
        
        if start_year and end_year:
            params['filters[dateYearRange][from]'] = str(start_year)
            params['filters[dateYearRange][to]'] = str(end_year)
    elif 'link.springer.com' in website:
        # Springer 期刊 - 多个期刊使用 OR 连接
        if len(journals) > 1:
            # 多个期刊合并，使用 OR 连接期刊名称
            journal_names = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    journal_name = JOURNAL_CONFIGS[journal]['params'].get('journal', '')
                    if journal_name:
                        journal_names.append( "\""+journal_name+"\"")
            params['journal'] = ' OR '.join(journal_names)
        # 单个期刊直接使用模板配置中的 journal
        
        if search_field == "Title":
            params['title'] = search_term
            # 清空 query 参数
            params['query'] = ""
        else:  # AllField
            params['query'] = search_term
            # 清空 title 参数
            params['title'] = ""
            
        if start_year and end_year:
            params['dateFrom'] = str(start_year)
            params['dateTo'] = str(end_year)
    elif 'tandfonline.com' in website:
        # Taylor & Francis 期刊 (JMIS) - 支持月份筛选
        if len(journals) > 1:
            # 多个期刊合并
            series_keys = []
            for journal in journals:
                if journal in JOURNAL_CONFIGS:
                    series_key = JOURNAL_CONFIGS[journal]['params'].get('SeriesKey', '')
                    if series_key:
                        series_keys.append(series_key)
            params['SeriesKey'] = ','.join(series_keys)
        # 单个期刊直接使用模板配置中的 SeriesKey
        
        params['text1'] = search_term
        if search_field == "Title":
            params['field1'] = "Title"
        elif search_field == "Abstract":
            params['field1'] = "Abstract"
        else:
            params['field1'] = "AllField"
            
        if start_year and end_year:
            params['AfterYear'] = start_year
            params['BeforeYear'] = end_year
    elif template_journal == "NBER":
        # NBER Working Papers - 支持日期筛选
        params['q'] = search_term
        
        # NBER使用YYYY-MM-DD格式的日期
        if start_year and end_year:
            # 构建开始日期
            start_date = f"{start_year}-{start_month:02d}-01" if start_month else f"{start_year}-01-01"
            
            # 构建结束日期
            if end_month:
                # 计算月份的最后一天
                if end_month in [1, 3, 5, 7, 8, 10, 12]:
                    last_day = 31
                elif end_month in [4, 6, 9, 11]:
                    last_day = 30
                else:  # 2月
                    # 简单处理闰年，2月按28天算
                    last_day = 28
                end_date = f"{end_year}-{end_month:02d}-{last_day:02d}"
            else:
                end_date = f"{end_year}-12-31"
                
            params['startDate'] = start_date
            params['endDate'] = end_date

    # 构建最终URL
    url_params = []
    
    # 为Oxford期刊使用特殊的URL编码方式
    if 'oup.com' in website:
        for key, value in params.items():
            if isinstance(value, list):
                for item in value:
                    url_params.append(f"{key}={urllib.parse.quote(str(item))}")
            elif value:
                # 对于Oxford期刊，某些参数需要特殊处理
                if key in ['cqb', 'qb']:
                    # JSON参数需要标准URL编码
                    encoded_value = urllib.parse.quote(str(value))
                    url_params.append(f"{key}={encoded_value}")
                elif key in ['rg_ArticleDate', 'rg_AllPublicationDates', 'rg_VersionDate']:
                    # 日期参数已经预编码，直接使用
                    url_params.append(f"{key}={value}")
                else:
                    url_params.append(f"{key}={urllib.parse.quote(str(value))}")
    elif 'publications.aaahq.org' in website:
        # AAA 期刊需要特殊的URL编码方式
        for key, value in params.items():
            if isinstance(value, list):
                for item in value:
                    url_params.append(f"{key}={urllib.parse.quote(str(item))}")
            elif value:
                if key == 'f_JournalDisplayName':
                    # 期刊名称使用+号替换空格
                    encoded_value = str(value).replace(' ', '+')
                    url_params.append(f"{key}={encoded_value}")
                elif key == 'qb':
                    # JSON参数使用标准URL编码
                    encoded_value = urllib.parse.quote(str(value))
                    url_params.append(f"{key}={encoded_value}")
                elif key == 'rg_PublicationDate':
                    # 日期参数保留空格
                    encoded_value = urllib.parse.quote(str(value), safe=' :T-')
                    url_params.append(f"{key}={encoded_value}")
                else:
                    url_params.append(f"{key}={urllib.parse.quote(str(value))}")
    elif 'nber.org' in website:
        # NBER Working Papers 特殊编码
        for key, value in params.items():
            if isinstance(value, list):
                for item in value:
                    url_params.append(f"{key}={urllib.parse.quote(str(item))}")
            elif value:
                if key == 'facet':
                    # facet参数需要特殊编码 contentType:working_paper -> contentType%3Aworking_paper
                    encoded_value = str(value).replace(':', '%3A')
                    url_params.append(f"{key}={encoded_value}")
                else:
                    url_params.append(f"{key}={urllib.parse.quote(str(value))}")
    else:
        # 其他网站使用标准编码
        for key, value in params.items():
            if isinstance(value, list):
                for item in value:
                    url_params.append(f"{key}={urllib.parse.quote(str(item))}")
            elif value:
                url_params.append(f"{key}={urllib.parse.quote(str(value))}")
    
    return f"{base_url}?{'&'.join(url_params)}"

def get_compatible_fields(selected_journals):
    """获取所选期刊的兼容搜索字段"""
    all_fields = set()
    for journal in selected_journals:
        if journal in JOURNAL_CONFIGS:
            all_fields.update(JOURNAL_CONFIGS[journal]['search_fields'])
    return list(all_fields)

# 主页面
def main():
    st.title("📚 Business Journal Search Tool")
    
    # 侧边栏 - 期刊选择
    st.sidebar.header("📋 Journal Selection")
    
    # 按领域分组期刊
    # https://ceibs.libguides.com/c.php?g=963339&p=7006250
    journal_groups = {
        "Operations Management": [
            "Management Science (MS)",
            "Production and Operations Management (POMS)",
            "Manufacturing & Service Operations Management (MSOM)",
            "Operations Research (OR)",
            "Journal of Operations Management (JOM)"
        ],
        "Finance": [
            "Journal of Finance (JF)",
            "Review of Financial Studies (RFS)",
            "Journal of Financial Economics (JFE)",
            "Journal of Financial and Quantitative Analysis (JFQA)",
            "Review of Finance (RF)"
        ],
        "Economics": [
            "American Economic Review (AER)",
            "Journal of Political Economy (JPE)",
            "Quarterly Journal of Economics (QJE)",
            "Review of Economic Studies (RES)",
            "Journal of International Economics (JIE)",
            "Econometrica",
            "NBER"
        ],
        "Accounting": [
            "The Accounting Review (AR)",
            "Journal of Accounting and Economics (JAE)",
            "Journal of Accounting Research (JAR)",
            "Contemporary Accounting Research (CAR)",
            "Review of Accounting Studies (RAS)",
            "Accounting, Organizations and Society (AOS)",
        ],
        "Information Systems": [
            "Information Systems Research (ISR)",
            "MIS Quarterly (MISQ)",
            "Journal on Computing (JC)",
            "Journal of Management Information Systems (JMIS)"
        ],
        "Management": [
            "Strategic Management Journal (SMJ)",
            "Academy of Management Journal (AMJ)",
            "Academy of Management Review (AMR)",
            "Administrative Science Quarterly (ASQ)",
            "Journal of Management (JM)",
            "Journal of Management Studies (JMS)",
             "Research Policy (RP)"
        ],
        "Organizational Behaviour": [
            "Organization Science (OS)",
            "Organization Studies (OS)",
            "Organizational Behavior and Human Decision Processes (OBHDP)"
        ],
        "Marketing": [
            "Marketing Science (MS)",
            "Journal of Consumer Research (JCR)",
            "Journal of Marketing (JM)",
            "Journal of Marketing Research (JMR)",
            "Journal of Consumer Psychology (JCP)",
            "Journal of the Academy of Marketing Science (JAMS)"
            
        ],
        "Human Resources": [
            "Human Relations (HR)",
            "Human Resource Management (HRM)"
        ],
        "Entrepreneurship": [
            "Entrepreneurship Theory and Practice (ETP)",
            "Journal of Business Venturing (JBV)",
            "Strategic Entrepreneurship Journal (SEJ)"
        ],
        "Others": [
            "Journal of International Business Studies (JIBS)",
            "Journal of Business Ethics (JBE)"
        ],
        
    }
    
    # 全选/清空按钮
    col1, col2, col3, col4 = st.sidebar.columns(4)
    select_all = col1.button("Pick All", key="select_all")
    clear_all = col2.button("Clear", key="clear_all")
    select_utd24 = col3.button("UTD24", key="select_utd24")
    select_ft50 = col4.button("FT50", key="select_ft50")

    # 添加一个小提示
    # st.sidebar.caption("💡 Tip: Click multiple category buttons to combine selections")

    col5, col6, col7, col8 = st.sidebar.columns(4)
    om_add = col5.button("OM", key="om_add")
    finance_add = col6.button("Finance", key="finance_add")
    econ_add = col7.button("Econ", key="econ_add")
    acc_add = col8.button("Acct", key="acc_add")

    # 初始化会话状态
    if 'selected_journals' not in st.session_state:
        st.session_state.selected_journals = []

    # 处理全选/清空按钮
    if select_all:
        st.session_state.selected_journals = [j for group in journal_groups.values() for j in group if j in JOURNAL_CONFIGS]

    if clear_all:
        st.session_state.selected_journals = []

    if select_utd24:
        st.session_state.selected_journals = list(set([j for j in UTD_24_JOURNALS if j in JOURNAL_CONFIGS]))

    if select_ft50:
        st.session_state.selected_journals = list(set([j for j in FT50_JOURNALS if j in JOURNAL_CONFIGS]))

    # 处理分类累加按钮 - 使用集合操作避免重复
    if om_add:
        om_journals = [j for j in journal_groups["Operations Management"] if j in JOURNAL_CONFIGS]
        st.session_state.selected_journals = list(set( om_journals))

    if finance_add:
        finance_journals = [j for j in journal_groups["Finance"] if j in JOURNAL_CONFIGS]
        st.session_state.selected_journals = list(set( finance_journals))

    if econ_add:
        econ_journals = [j for j in journal_groups["Economics"] if j in JOURNAL_CONFIGS]
        st.session_state.selected_journals = list(set( econ_journals))

    if acc_add:
        acc_journals = [j for j in journal_groups["Accounting"] if j in JOURNAL_CONFIGS]
        st.session_state.selected_journals = list(set( acc_journals))


    # 期刊复选框
    for group_name, journals in journal_groups.items():
        st.sidebar.subheader(group_name)
        for journal in journals:
             if journal in JOURNAL_CONFIGS:
                
                # st.sidebar.write(journal)
                # st.sidebar.write(journal in st.session_state.selected_journals)
                t = st.sidebar.checkbox(
                    journal,
                    value=(journal in st.session_state.selected_journals),
                    key=f"{journal}",
                    on_change=update_journal_selection,
                    args=(journal,)
                )
                # st.sidebar.write(t)

    # 从 session_state 获取最终的选中列表
    selected_journals = st.session_state.selected_journals

    
    # 主区域 - 搜索设置
    st.header("🔍 Search Settings")
    
    # 第一行：搜索关键词和搜索字段
    col1, col2 = st.columns([3, 1])
    with col1:
        # 搜索关键词
        search_term = st.text_area(
            "Search Keywords",
            placeholder="Enter search keywords...",
            height=80
        )
    
    with col2:
        # 搜索字段选择
        if selected_journals:
            compatible_fields = get_compatible_fields(selected_journals)
            search_field = st.selectbox(
                "Search Field",
                options=compatible_fields,
                index=0 if compatible_fields else 0
            )
        else:
            search_field = st.selectbox(
                "Search Field",
                options=["AllField", "Title", "Abstract"],
                index=0
            )
    
    # 第二行：时间范围
    st.header("🗓️ Date Range")
    current_year = datetime.now().year
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # 起始年份
        start_year = st.number_input(
            "Start Year",
            min_value=1900,
            max_value=current_year + 10,
            value=current_year - 5
        )
    
    with col2:
        # 起始月份
        start_month = st.selectbox(
            "Start Month",
            options=list(range(1, 13)),
            format_func=lambda x: f"{x}",
            index=0
        )
    
    with col3:
        # 结束年份
        end_year = st.number_input(
            "End Year",
            min_value=1900,
            max_value=current_year + 10,
            value=current_year
        )
    
    with col4:
        # 结束月份
        end_month = st.selectbox(
            "End Month",
            options=list(range(1, 13)),
            format_func=lambda x: f"{x}",
            index=11
        )
    
    # 显示已选择的期刊
    if selected_journals:
        st.info(f"Selected {len(selected_journals)} journals: {', '.join([j.split(' (')[0] for j in selected_journals])}")
    else:
        st.warning("Please select at least one journal")
    
    # 搜索按钮
    if st.button("🔍 Generate Search Links", type="primary", disabled=not selected_journals or not search_term):
        if not selected_journals:
            st.error("⚠️ Please select at least one journal!")
        elif not search_term.strip():
            st.error("⚠️ Please enter search keywords!")
        else:
            
            # 按网站分组期刊
            website_groups = group_journals_by_website(selected_journals)
            
            urls_info = []
            all_urls = []
            
            for website, journals in website_groups.items():
                # st.write(f"**📡 处理网站: {website}**")
                
                # 统一使用合并搜索逻辑
                combined_url = generate_combined_search_url(
                    journals, search_term.strip(), search_field, start_year, end_year,
                    start_month, end_month
                )
                
                if combined_url:
                    if len(journals) == 1:
                        # 单个期刊显示
                        journal_display_name = journals[0].split(' (')[0]
                        urls_info.append(f"**🔗 {journal_display_name}:**\n{combined_url}")
                    else:
                        # 多个期刊显示
                        journal_names = ", ".join([j.split(' (')[0] for j in journals])
                        urls_info.append(f"**🔗 Combined Search ({journal_names}):**\n{combined_url}")
                    all_urls.append(combined_url)
            
            if all_urls:
                 # 显示生成的URLs和批量操作按钮
                 header_col1, header_col2, header_col3,_ = st.columns([.9, 0.6, 0.6,2])
                 with header_col1:
                     st.header("📋 Search Links")
                 
                 with header_col2:
                     # 全部复制按钮
                     all_urls_text = '\\n\\n'.join([f"{urls_info[i].split(chr(10))[0].replace('**🔗 ', '').replace(':**', '')}:\\n{url}" for i, url in enumerate(all_urls)])
                     copy_all_js = f"""
                     <script>
                     function copyAllToClipboard() {{
                         var allUrlsText = `{all_urls_text}`;
                         navigator.clipboard.writeText(allUrlsText);
                     }}
                     </script>
                     <button onclick="copyAllToClipboard()" style="
                         background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                         border: none;
                         color: white;
                         padding: 8px 16px;
                         text-align: center;
                         text-decoration: none;
                         display: inline-block;
                         font-size: 14px;
                         margin: 4px 2px;
                         cursor: pointer;
                         border-radius: 8px;
                         font-weight: 500;
                         box-shadow: 0 2px 4px rgba(79, 172, 254, 0.2);
                         transition: all 0.3s ease;
                         text-shadow: 0 1px 2px rgba(0,0,0,0.1);
                     " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(79, 172, 254, 0.3)'" 
                       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(79, 172, 254, 0.2)'">📋 Copy All</button>
                     """
                     components.html(copy_all_js, height=50)
                 
                 with header_col3:
                     # 全部打开按钮
                     open_all_js = f"""
                     <script>
                     function openAllLinks() {{
                         var urls = {str(all_urls).replace("'", '"')};
                         var delay = 500; // 每个页面间隔500毫秒打开
                         
                         urls.forEach(function(url, index) {{
                             setTimeout(function() {{
                                 window.open(url, '_blank');
                             }}, index * delay);
                         }});
                     }}
                     </script>
                     <button onclick="openAllLinks()" style="
                         background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                         border: none;
                         color: white;
                         padding: 8px 16px;
                         text-align: center;
                         text-decoration: none;
                         display: inline-block;
                         font-size: 14px;
                         margin: 4px 2px;
                         cursor: pointer;
                         border-radius: 8px;
                         font-weight: 500;
                         box-shadow: 0 2px 4px rgba(250, 112, 154, 0.2);
                         transition: all 0.3s ease;
                         text-shadow: 0 1px 2px rgba(0,0,0,0.1);
                     " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(250, 112, 154, 0.3)'" 
                       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(250, 112, 154, 0.2)'">🚀 Open All</button>
                     """
                     components.html(open_all_js, height=50)
                 
                 # 显示每个搜索链接及其操作按钮
                 for i, url_info in enumerate(urls_info):
                     # 从url_info中提取期刊名称作为标题
                     lines = url_info.split('\n')
                     title_line = lines[0].replace('**🔗 ', '').replace(':**', '')
                     
                     with st.expander(f"🔗 {title_line}", expanded=True):
                         if len(lines) > 1:
                             st.code(lines[1], language='text')
                             
                             # 为每个链接添加操作按钮
                             col1, col2, col3 = st.columns([1, 1, 4])
                             with col1:
                                 # 复制链接按钮
                                 copy_js = f"""
                                 <script>
                                 function copyToClipboard{i}() {{
                                     navigator.clipboard.writeText('{all_urls[i]}');
                                 }}
                                 </script>
                                 <button onclick="copyToClipboard{i}()" style="
                                     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                     border: none;
                                     color: white;
                                     padding: 8px 16px;
                                     text-align: center;
                                     text-decoration: none;
                                     display: inline-block;
                                     font-size: 14px;
                                     margin: 4px 2px;
                                     cursor: pointer;
                                     border-radius: 8px;
                                     font-weight: 500;
                                     box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                     transition: all 0.3s ease;
                                 " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)'" 
                                   onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'">📋 Copy</button>
                                 """
                                 components.html(copy_js, height=50)
                             
                             with col2:
                                 # 打开链接按钮
                                 open_js = f"""
                                 <button onclick="window.open('{all_urls[i]}', '_blank')" style="
                                     background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                     border: none;
                                     color: white;
                                     padding: 8px 16px;
                                     text-align: center;
                                     text-decoration: none;
                                     display: inline-block;
                                     font-size: 14px;
                                     margin: 4px 2px;
                                     cursor: pointer;
                                     border-radius: 8px;
                                     font-weight: 500;
                                     box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                     transition: all 0.3s ease;
                                 " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)'" 
                                   onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'">🔗 Open</button>
                                 """
                                 components.html(open_js, height=50)

            else:
                st.error("❌ Failed to generate URLs!")

if __name__ == "__main__":
    main()
