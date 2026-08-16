import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    # Em dashes
    '\u00e2\u0080\u0094': '&mdash;',   # â€" → —
    '\u00e2\u0080\u0093': '&ndash;',   # â€" → –
    # Middle dot / bullet
    '\u00c2\u00b7': '&middot;',         # Â· → ·
    '\u00c2\u00a0': ' ',                # Â  (non-breaking space)
    '\u00c2\u00a9': '&copy;',           # Â© → ©
    # Smart quotes
    '\u00e2\u0080\u0099': '&rsquo;',    # â€™ → '
    '\u00e2\u0080\u0098': '&lsquo;',    # â€˜ → '
    '\u00e2\u0080\u009c': '&ldquo;',    # â€œ → "
    '\u00e2\u0080\u009d': '&rdquo;',    # â€  → "
    # Emojis → FontAwesome icons
    '\u00f0\u009f\u0093\u00a2': '<i class="fas fa-bullhorn"></i>',      # 📢
    '\u00f0\u009f\u008f\u0086': '<i class="fas fa-trophy"></i>',        # 🏆
    '\u00f0\u009f\u0093\u009a': '<i class="fas fa-book"></i>',          # 📚
    '\u00f0\u009f\u008c\u00bf': '<i class="fas fa-leaf"></i>',          # 🌿
    '\u00f0\u009f\u0093\u009d': '<i class="fas fa-clipboard-list"></i>',# 📝
    '\u00f0\u009f\u0093\u0096': '<i class="fas fa-book-open"></i>',     # 📖
    '\u00f0\u009f\u0093\u009c': '<i class="fas fa-scroll"></i>',        # 📜
    '\u00f0\u009f\u0094\u00ac': '<i class="fas fa-microscope"></i>',    # 🔬
    '\u00f0\u009f\u008c\u008d': '<i class="fas fa-globe"></i>',         # 🌍
    '\u00f0\u009f\u0092\u00bb': '<i class="fas fa-laptop"></i>',        # 💻
    '\u00f0\u009f\u008e\u00a8': '<i class="fas fa-palette"></i>',       # 🎨
    '\u00f0\u009f\u008f\u0083': '<i class="fas fa-running"></i>',       # 🏃
    '\u00e2\u009a\u0097\u00ef\u00b8\u008f': '<i class="fas fa-flask"></i>',  # ⚗️
    '\u00e2\u009a\u0097\ufe0f': '<i class="fas fa-flask"></i>',
    '\u00f0\u009f\u0095\u008c': '<i class="fas fa-mosque"></i>',        # 🕌
}

for bad, good in replacements.items():
    content = content.replace(bad, good)

# Also fix literal mojibake strings that appear in file as-is
literal_fixes = [
    ('â€"',  '&mdash;'),
    ('â€"',  '&mdash;'),
    ('Â·',   '&middot;'),
    ('Â©',   '&copy;'),
    ('Â',    ''),
    ('â€™',  '&rsquo;'),
    ('â€˜',  '&lsquo;'),
    ('â€œ',  '&ldquo;'),
    ('â€',   '&rdquo;'),
    ('ðŸ"¢', '<i class="fas fa-bullhorn"></i>'),
    ('ðŸ†',  '<i class="fas fa-trophy"></i>'),
    ('ðŸ"š', '<i class="fas fa-book"></i>'),
    ('ðŸŒ¿', '<i class="fas fa-leaf"></i>'),
    ('ðŸ"',  '<i class="fas fa-clipboard-list"></i>'),
    ('ðŸ"–', '<i class="fas fa-book-open"></i>'),
    ('ðŸ"œ', '<i class="fas fa-scroll"></i>'),
    ('ðŸ"¬', '<i class="fas fa-microscope"></i>'),
    ('ðŸŒ',  '<i class="fas fa-globe"></i>'),
    ('ðŸ'»', '<i class="fas fa-laptop"></i>'),
    ('ðŸŽ¨', '<i class="fas fa-palette"></i>'),
    ('ðŸƒ',  '<i class="fas fa-running"></i>'),
    ('ðŸ•Œ', '<i class="fas fa-mosque"></i>'),
    ('â€"',  '&mdash;'),
    ('â€"',  '&mdash;'),
]

for bad, good in literal_fixes:
    content = content.replace(bad, good)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Fixed all encoding issues.")
