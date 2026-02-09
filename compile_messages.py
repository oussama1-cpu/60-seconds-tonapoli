#!/usr/bin/env python
"""Compile .po files to .mo files without GNU gettext"""
import struct
import array
import os
from pathlib import Path

def compile_po_to_mo(po_path, mo_path):
    """Compile a .po file to a .mo file"""
    messages = {}
    
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse .po file
    current_msgid = None
    current_msgstr = None
    
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('msgid "'):
            current_msgid = line[7:-1]
            # Check for multiline
            while i + 1 < len(lines) and lines[i + 1].strip().startswith('"'):
                i += 1
                current_msgid += lines[i].strip()[1:-1]
        elif line.startswith('msgstr "'):
            current_msgstr = line[8:-1]
            # Check for multiline
            while i + 1 < len(lines) and lines[i + 1].strip().startswith('"'):
                i += 1
                current_msgstr += lines[i].strip()[1:-1]
            
            if current_msgid and current_msgstr:
                messages[current_msgid] = current_msgstr
            current_msgid = None
            current_msgstr = None
        
        i += 1
    
    # Generate .mo file
    keys = sorted(messages.keys())
    offsets = []
    ids = b''
    strs = b''
    
    for key in keys:
        # Offset for msgid
        offsets.append((len(ids), len(key.encode('utf-8')), len(strs), len(messages[key].encode('utf-8'))))
        ids += key.encode('utf-8') + b'\x00'
        strs += messages[key].encode('utf-8') + b'\x00'
    
    # Generate the hash table (empty for simplicity)
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    
    output = []
    # Magic number
    output.append(struct.pack('I', 0x950412de))
    # Version
    output.append(struct.pack('I', 0))
    # Number of strings
    output.append(struct.pack('I', len(keys)))
    # Offset of table with original strings
    output.append(struct.pack('I', 7 * 4))
    # Offset of table with translation strings
    output.append(struct.pack('I', 7 * 4 + len(keys) * 8))
    # Size of hashing table
    output.append(struct.pack('I', 0))
    # Offset of hashing table
    output.append(struct.pack('I', 0))
    
    # Original string table
    for o in offsets:
        output.append(struct.pack('II', o[1], keystart + o[0]))
    
    # Translation string table
    for o in offsets:
        output.append(struct.pack('II', o[3], valuestart + o[2]))
    
    # Strings
    output.append(ids)
    output.append(strs)
    
    with open(mo_path, 'wb') as f:
        f.write(b''.join(output))
    
    print(f"Compiled: {po_path} -> {mo_path}")

if __name__ == '__main__':
    locale_dir = Path('locale')
    for po_file in locale_dir.glob('*/LC_MESSAGES/django.po'):
        mo_file = po_file.with_suffix('.mo')
        try:
            compile_po_to_mo(str(po_file), str(mo_file))
        except Exception as e:
            print(f"Error compiling {po_file}: {e}")
