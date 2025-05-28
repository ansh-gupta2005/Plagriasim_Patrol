import html
import difflib
def highlight_matches(text1, text2):
    matcher = difflib.SequenceMatcher(None, text1, text2)
    matched_text1 = ""
    matched_text2 = ""

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            matched_text1 += f'<span style="background-color: #c6f6d5">{text1[i1:i2]}</span>'
            matched_text2 += f'<span style="background-color: #c6f6d5">{text2[j1:j2]}</span>'
        else:
            matched_text1 += text1[i1:i2]
            matched_text2 += text2[j1:j2]

    return matched_text1, matched_text2
