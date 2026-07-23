#!/usr/bin/env python3
"""
GLOW IDE - Terminal editor postaveny na prompt_toolkit
Zadne blikani, zadny lag. Bezpecna, popularni knihovna.
"""

import os
import sys
from pathlib import Path

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window, FloatContainer, Float
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar
from prompt_toolkit.filters import Condition


class GlowEditor:
    def __init__(self, filename=None):
        self.filename = filename
        self.modified = False
        self.message = ""
        
        # Nacteni souboru
        if filename and os.path.exists(filename):
            with open(filename, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        else:
            text = ""
        
        # Vytvoreni bufferu
        search = SearchToolbar()
        self.buffer = Buffer(
            text=text,
            multiline=True,
            search=search,
            on_text_changed=self._on_text_changed
        )
        
        self.search = search
        self.status_text = ""
        
        # Keybindings
        kb = self._create_keybindings()
        
        # Styly
        style = Style.from_dict({
            "status": "reverse",
            "status.mode": "bg:#444444 #ffffff bold",
            "status.file": "bg:#0044aa #ffffff",
            "status.modified": "bg:#aa0000 #ffffff bold",
            "status.saved": "bg:#006600 #ffffff",
            "line-numbers": "#666666",
            "line-numbers.current": "#ffaa00 bold",
            "message": "bg:#222222 #00ff00",
        })
        
        # Layout
        self.layout = self._create_layout()
        
        # Application
        self.application = Application(
            layout=Layout(self.layout),
            key_bindings=kb,
            style=style,
            full_screen=True,
            mouse_support=True,
        )
    
    def _on_text_changed(self, _buffer):
        self.modified = True
    
    def _get_line_numbers(self):
        """Vrati cisla radku jako formatted text"""
        text = self.buffer.text
        cursor_row = self.buffer.document.cursor_position_row
        
        lines = []
        for i in range(text.count("\n") + 1):
            if i == cursor_row:
                lines.append(("class:line-numbers.current", f"{i+1:4}\n"))
            else:
                lines.append(("class:line-numbers", f"{i+1:4}\n"))
        
        return lines
    
    def _get_status_bar(self):
        """Status bar dole"""
        cursor = self.buffer.document.cursor_position
        row = self.buffer.document.cursor_position_row + 1
        col = self.buffer.document.cursor_position_col + 1
        total = self.buffer.text.count("\n") + 1
        
        fname = self.filename or "Novy soubor"
        
        result = []
        result.append(("class:status", " "))
        result.append(("class:status.file", f" {fname} "))
        
        if self.modified:
            result.append(("class:status.modified", " [+modified] "))
        else:
            result.append(("class:status.saved", " [saved] "))
        
        result.append(("class:status", f" Radek {row}/{total} Sloupec {col} "))
        result.append(("class:status", "   Ctrl+S=save Ctrl+Q=quit Ctrl+O=open "))
        
        return result
    
    def _create_layout(self):
        """Vytvori layout editoru"""
        # Editor s cisly radku
        editor = Window(
            content=BufferControl(buffer=self.buffer),
            left_margin=FormattedTextControl(text=self._get_line_numbers()),
            wrap_lines=False,
        )
        
        # Status bar
        status_bar = Window(
            content=FormattedTextControl(text=self._get_status_bar),
            height=Dimension.exact(1),
            style="class:status",
        )
        
        # Help bar
        help_bar = Window(
            content=FormattedTextControl(
                text=" Ctrl+S=save Ctrl+Q=quit Ctrl+O=open Ctrl+G=goto :commands | GLOW IDE"
            ),
            height=Dimension.exact(1),
            style="class:status.mode",
        )
        
        return HSplit([editor, status_bar, help_bar])
    
    def _create_keybindings(self):
        """Klavesove zkratky"""
        kb = KeyBindings()
        
        @kb.add("c-q")
        def _(event):
            """Ctrl+Q - ukoncit"""
            if self.modified:
                event.app.layout.focus(self.buffer)
                self.buffer.text = self.buffer.text
                # Zeptat se
                from prompt_toolkit.shortcuts import yes_no_dialog
                # Jednodussi - jen ulozit a ukoncit
                self.message = "Ctrl+Y=ulozit a ukoncit | Ctrl+N=ukoncit bez ulozeni | Esc=zrusit"
                event.app.invalidate()
            else:
                event.app.exit()
        
        @kb.add("c-y", filter=Condition(lambda: self.modified))
        def _(event):
            """Ctrl+Y - ulozit a ukoncit (po Ctrl+Q)"""
            if self.filename:
                self._save()
            event.app.exit()
        
        @kb.add("c-n", filter=Condition(lambda: self.modified))
        def _(event):
            """Ctrl+N - ukoncit bez ulozeni (po Ctrl+Q)"""
            event.app.exit()
        
        @kb.add("c-s")
        def _(event):
            """Ctrl+S - ulozit"""
            if self.filename:
                self._save()
                self.modified = False
                self.message = f"Ulozeno: {self.filename}"
            else:
                # Save as - jednoduchy prompt
                from prompt_toolkit.shortcuts import input_dialog
                result = input_dialog(
                    title="Ulozit jako",
                    text="Zadej nazev souboru:"
                ).run()
                if result:
                    self.filename = result
                    self._save()
                    self.modified = False
                    self.message = f"Ulozeno: {result}"
            event.app.invalidate()
        
        @kb.add("c-o")
        def _(event):
            """Ctrl+O - otevrit"""
            from prompt_toolkit.shortcuts import input_dialog
            result = input_dialog(
                title="Otevrit soubor",
                text="Zadej cestu k souboru:"
            ).run()
            if result and os.path.exists(result):
                with open(result, "r", encoding="utf-8", errors="replace") as f:
                    self.buffer.text = f.read()
                self.filename = result
                self.modified = False
                self.message = f"Otevreno: {result}"
            elif result:
                self.message = f"Soubor nenalezen: {result}"
            event.app.invalidate()
        
        @kb.add("c-g")
        def _(event):
            """Ctrl+G - skocit na radek"""
            from prompt_toolkit.shortcuts import input_dialog
            result = input_dialog(
                title="Skocit na radek",
                text="Zadej cislo radku:"
            ).run()
            if result and result.isdigit():
                line_num = int(result)
                lines = self.buffer.text.split("\n")
                if 1 <= line_num <= len(lines):
                    # Spocitat pozici
                    pos = sum(len(l) + 1 for l in lines[:line_num - 1])
                    self.buffer.cursor_position = pos
                    self.message = f"Radek {line_num}"
                else:
                    self.message = "Radek neexistuje"
            event.app.invalidate()
        
        @kb.add("escape", "escape")
        def _(event):
            """Esc Esc - zrusit mod"""
            self.message = ""
            event.app.invalidate()
        
        return kb
    
    def _save(self):
        """Ulozi soubor"""
        if not self.filename:
            return
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(self.buffer.text)
        except Exception as e:
            self.message = f"Chyba pri ulozeni: {e}"
    
    def run(self):
        """Spusti editor"""
        self.application.run()


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    editor = GlowEditor(filename)
    editor.run()


if __name__ == "__main__":
    main()
