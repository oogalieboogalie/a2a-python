# File Processing Agent

This example demonstrates how to build an A2A agent that processes files and documents. It showcases:

- 📁 Binary data handling 
- 🔄 Multiple input formats (text, JSON, CSV)
- 📊 File analysis and processing
- 📤 Artifact creation with processed results
- 🏷️ Metadata extraction and enrichment

## 🎯 What This Agent Does

The File Processing Agent can:

1. **Analyze Text Files** - Count words, lines, characters, and extract metadata
2. **Process JSON Files** - Parse, validate, and extract structured information
3. **Handle CSV Files** - Analyze columns, row counts, and data types
4. **Extract Metadata** - File size, type detection, encoding analysis
5. **Generate Reports** - Comprehensive analysis reports with statistics

## 🚀 Quick Start

### 1. Install Dependencies

From the project root:
```bash
pip install -e ".[http-server]"
# Optional: For enhanced file type detection
pip install python-magic
```

### 2. Run the Agent

```bash
cd examples/file-processor
python agent.py
```

### 3. Test the Agent

```bash
# Test with sample files
python test_client.py

# Or test specific file types
python test_client.py --text
python test_client.py --json
python test_client.py --csv
```

## 📁 Files in This Example

- **`agent.py`** - Main file processing agent
- **`test_client.py`** - Test client with sample files
- **`sample_files/`** - Sample files for testing
- **`README.md`** - This documentation
- **`requirements.txt`** - Optional dependencies

## 🔍 Key Concepts Demonstrated

### 1. Binary Data Handling

```python
# Handle uploaded files
data_content = part.root.data  # Binary data
file_info = analyze_binary_data(data_content)
```

### 2. Multiple Input Modes

```python
AgentSkill(
    id="file_analyzer",
    name="File Analysis",
    description="Analyze various file types and extract information",
    inputModes=[
        "text/plain",
        "application/json", 
        "text/csv",
        "application/octet-stream"
    ],
    outputModes=["application/json", "text/plain"]
)
```

### 3. File Type Detection

```python
def detect_file_type(data: bytes, filename: str = None) -> str:
    """Detect file type from content and filename."""
    # Magic number detection
    if data.startswith(b'{"') or data.startswith(b'['):
        return "application/json"
    # ... more detection logic
```

### 4. Structured Results

```python
analysis_result = {
    "file_info": {
        "size": len(data),
        "type": detected_type,
        "encoding": detected_encoding
    },
    "content_analysis": {
        "word_count": word_count,
        "line_count": line_count,
        "statistics": stats
    }
}
```

## 🧪 Testing Scenarios

### Text File Analysis
```python
# Upload a text file and get word count, line analysis
await client.send_file("sample.txt", "Analyze this text file")
```

### JSON Processing
```python
# Validate and analyze JSON structure
await client.send_file("data.json", "Process this JSON file")
```

### CSV Analysis
```python
# Get column info, row counts, data types
await client.send_file("data.csv", "Analyze this CSV file")
```

## 🔧 Customization Ideas

### Add New File Types
```python
# Support for more formats
elif detected_type == "application/xml":
    return analyze_xml_content(content)
elif detected_type == "image/jpeg":
    return analyze_image_metadata(data)
```

### Enhanced Analysis
```python
# Add sentiment analysis for text
from textblob import TextBlob
sentiment = TextBlob(text_content).sentiment

# Add data quality checks for CSV
quality_score = assess_data_quality(csv_data)
```

### Async Processing
```python
# For large files, use streaming
async def process_large_file(self, file_data):
    # Process in chunks
    for chunk in chunk_data(file_data, chunk_size=1024*1024):
        result = await process_chunk(chunk)
        yield partial_result
```

## 📚 Related Examples

- 🔤 [Simple Echo Agent](../simple-echo-agent/) - Basic message patterns
- 🎯 [Multi-Skill Agent](../multi-skill-agent/) - Multiple capabilities  
- 🚀 [Production Template](../production-template/) - Full deployment setup

---

**Ready to process some files?** 📂✨