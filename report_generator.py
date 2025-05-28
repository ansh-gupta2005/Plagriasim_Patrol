import pandas as pd
from datetime import datetime
import json
import os

def generate_comparison_report(file1_name, file2_name, similarity_score, text_stats1, text_stats2, 
                             citations1, citations2, ngram_sim=None, paraphrase_score=None):
    """Generate a detailed comparison report."""
    report = {
        "report_metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "files_compared": [file1_name, file2_name]
        },
        "similarity_analysis": {
            "overall_similarity": f"{similarity_score:.2f}%",
            "ngram_similarity": f"{ngram_sim:.2f}" if ngram_sim is not None else "N/A",
            "paraphrase_detection_score": f"{paraphrase_score:.2f}" if paraphrase_score is not None else "N/A"
        },
        "document_statistics": {
            file1_name: text_stats1,
            file2_name: text_stats2
        },
        "citations_found": {
            file1_name: citations1,
            file2_name: citations2
        }
    }
    return report

def save_report_json(report, output_dir="reports"):
    """Save the report in JSON format."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plagiarism_report_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=4)
    
    return filepath

def save_report_excel(report, output_dir="reports"):
    """Save the report in Excel format with multiple sheets."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plagiarism_report_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    # Create Excel writer
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        # Metadata sheet
        pd.DataFrame([report["report_metadata"]]).to_excel(writer, sheet_name='Metadata', index=False)
        
        # Similarity Analysis sheet
        pd.DataFrame([report["similarity_analysis"]]).to_excel(writer, sheet_name='Similarity Analysis', index=False)
        
        # Document Statistics sheet
        stats_df = pd.DataFrame(report["document_statistics"])
        stats_df.to_excel(writer, sheet_name='Document Statistics')
        
        # Citations sheet
        citations_df = pd.DataFrame(report["citations_found"])
        citations_df.to_excel(writer, sheet_name='Citations Found')
    
    return filepath

def generate_html_report(report):
    """Generate an HTML version of the report."""
    html = f"""
    <html>
    <head>
        <title>Plagiarism Check Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
            .header {{ background-color: #f8f9fa; padding: 10px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #f8f9fa; }}
        </style>
    </head>
    <body>
        <h1>Plagiarism Check Report</h1>
        
        <div class="section">
            <h2>Report Metadata</h2>
            <p><strong>Generated at:</strong> {report["report_metadata"]["generated_at"]}</p>
            <p><strong>Files Compared:</strong> {', '.join(report["report_metadata"]["files_compared"])}</p>
        </div>
        
        <div class="section">
            <h2>Similarity Analysis</h2>
            <table>
                <tr><th>Metric</th><th>Score</th></tr>
                <tr><td>Overall Similarity</td><td>{report["similarity_analysis"]["overall_similarity"]}</td></tr>
                <tr><td>N-gram Similarity</td><td>{report["similarity_analysis"]["ngram_similarity"]}</td></tr>
                <tr><td>Paraphrase Detection</td><td>{report["similarity_analysis"]["paraphrase_detection_score"]}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Document Statistics</h2>
            <table>
                <tr><th>Metric</th>
                    <th>{report["report_metadata"]["files_compared"][0]}</th>
                    <th>{report["report_metadata"]["files_compared"][1]}</th></tr>
    """
    
    # Add document statistics
    for metric in report["document_statistics"][report["report_metadata"]["files_compared"][0]].keys():
        html += f"""
                <tr>
                    <td>{metric}</td>
                    <td>{report["document_statistics"][report["report_metadata"]["files_compared"][0]][metric]}</td>
                    <td>{report["document_statistics"][report["report_metadata"]["files_compared"][1]][metric]}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Citations Found</h2>
    """
    
    for file_name in report["citations_found"]:
        html += f"""
            <h3>{file_name}</h3>
            <ul>
        """
        for citation in report["citations_found"][file_name]:
            html += f"<li>{citation}</li>"
        html += "</ul>"
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

def save_report_html(report, output_dir="reports"):
    """Save the report in HTML format."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plagiarism_report_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)
    
    html_content = generate_html_report(report)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath 