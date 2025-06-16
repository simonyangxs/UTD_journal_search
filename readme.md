# 📚 UTD Journal Search Tool

## 🌐 Live Demo
**Try the tool online:** [https://utdjournalsearch.streamlit.app/](https://utdjournalsearch.streamlit.app/)

## 📖 User Guide

### 🚀 Quick Start
1. **Select Journals**: Check the journals you want to search in the journal list (supports multiple selections)
2. **Review Selection**: Selected journals will be displayed in the "Selected Journals" text box
3. **Enter Search Keywords**: Input your search keywords in the text box
4. **Choose Search Field**: Select whether to search in title, abstract, or full text
5. **Set Date Range**: If supported by the journal, you can set start and end years
6. **Start Search**: Click the search button, the system will intelligently merge journals from the same website and open search pages

### ✅ Journal Selection Features

**Checkbox Selection**:
- Journals are grouped by field (Operations Management + Information Systems, Economics, Finance + Accounting, Management)
- Simply check the checkbox to select journals
- Supports cross-field multiple selections

**Convenient Operations**:
- **Select All Button**: Select all journals with one click
- **Clear All Button**: Clear all selections with one click
- **Real-time Display**: Selected journals are displayed in real-time in the selection box


### 📚 Journal Details

#### 🔧 Operations Management + Information Systems
| Journal Name | Abbreviation | Website | Field Filtering | Date Filtering |
|--------------|--------------|---------|----------------|----------------|
| Management Science | MS | INFORMS | Title/All Fields | ✅ |
| Manufacturing & Service Operations Management | MSOM | INFORMS | Title/All Fields | ✅ |
| Production and Operations Management | POMS | Sage | Title/Abstract/All Fields | ✅ |
| Information Systems Research | ISR | INFORMS | Title/All Fields | ✅ |
| MIS Quarterly | MISQ | MISQ | Title/Abstract | ✅ |

#### 📊 Economics
| Journal Name | Abbreviation | Website | Field Filtering | Date Filtering |
|--------------|--------------|---------|----------------|----------------|
| American Economic Review | AER | AEA | Title/Abstract | ❌ |
| Quarterly Journal of Economics | QJE | Oxford | Title/Abstract/All Fields | ✅ |
| Journal of Political Economy | JPE | Chicago | Title/All Fields | ✅ |
| Journal of International Economics | JIE | ScienceDirect | Title/All Fields | ✅ |
| Review of Economic Studies | RES | Oxford | Title/Abstract/All Fields | ✅ |

#### 💰 Finance + Accounting
| Journal Name | Abbreviation | Website | Field Filtering | Date Filtering |
|--------------|--------------|---------|----------------|----------------|
| Journal of Finance | JF | Wiley | Title/Abstract/All Fields | ✅ |
| Review of Financial Studies | RFS | Oxford | Title/Abstract/All Fields | ✅ |
| Journal of Financial Economics | JFE | ScienceDirect | Title/All Fields | ✅ |
| Journal of Accounting Research | JAR | Wiley | Title/Abstract/All Fields | ✅ |
| Journal of Accounting and Economics | JAE | ScienceDirect | Title/All Fields | ✅ |
| The Accounting Review | AR | AAA | Title/Abstract/All Fields | ✅ |

#### 🏢 Management
| Journal Name | Abbreviation | Website | Field Filtering | Date Filtering |
|--------------|--------------|---------|----------------|----------------|
| Organization Science | OS | INFORMS | Title/All Fields | ✅ |
| Strategic Management Journal | SMJ | Wiley | Title/Abstract/All Fields | ✅ |
| Administrative Science Quarterly | ASQ | Sage | Title/Abstract/All Fields | ✅ |
| Academy of Management Journal | AMJ | AOM | Title/Abstract/All Fields | ✅ |

## Comparison with Similar Products:
- [econ-paper-search](https://econ-paper-search.streamlit.app/): Mainly focuses on econ papers, cannot guarantee real-time article updates
- [gotostudies](https://www.gotostudies.com/): Uses Google Scholar search, but has lower accuracy and completeness in journal coverage
