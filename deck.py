"""Tiny Snakes On A Board presentation.

This file is both the manim-slides deck and a marimo notebook
(pattern from marimo's "Manim Slides is plain awesome" video):

    make render     low quality, fast iteration
    make present    live Qt presenter
    make html       self-contained reveal.js file
    make notebook   edit reactively: change Deck, preview re-renders inline

Pick a colour scheme with the dropdown in the notebook, or from the shell:

    DECK_PALETTE=wax make render

Run from the repo root so the relative fonts/ path resolves.
"""

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

with app.setup:
    import os
    from pathlib import Path

    import manimpango
    import numpy as np
    from manim import (
        BOLD,
        DEGREES,
        DOWN,
        LEFT,
        NORMAL,
        ORIGIN,
        PI,
        RIGHT,
        TAU,
        UP,
        AddTextLetterByLetter,
        Animation,
        AnimationGroup,
        Arc,
        Arrow,
        Axes,
        Brace,
        Broadcast,
        Circle,
        Circumscribe,
        Create,
        Cross,
        CurvedArrow,
        DashedLine,
        DecimalNumber,
        Dot,
        FadeIn,
        FadeOut,
        Flash,
        Group,
        GrowFromCenter,
        ImageMobject,
        Indicate,
        LaggedStart,
        Line,
        ManimColor,
        MoveAlongPath,
        ParametricFunction,
        Polygon,
        RoundedRectangle,
        SVGMobject,
        Sector,
        ShrinkToCenter,
        Succession,
        Text,
        TransformMatchingShapes,
        VGroup,
        VMobject,
        Write,
        config,
        linear,
        rush_into,
        smooth,
    )
    from manim.utils.rate_functions import ease_out_expo
    from manim_slides import Slide

    for _ttf in Path("fonts").glob("*.ttf"):
        manimpango.register_font(str(_ttf))

    FONT = "TT2020Base"

    PALETTES = {
        "wax": {
            "bg": "#f5f0e8", "title": "#1b232c", "body": "#2b3642", "accent": "#c95750",
        },
        "pine": {
            "bg": "#21302c", "title": "#eafff4", "body": "#bfd7ce", "accent": "#8fe6c0",
        },
        "dawn": {
            "bg": "#ebf2f7", "title": "#1a242a", "body": "#303e47", "accent": "#00788b",
        },
        "dusk": {
            "bg": "#243037", "title": "#e3ddd7", "body": "#c1b8b0", "accent": "#7bbac7",
        },
    }
    PALETTE = PALETTES.get(os.environ.get("DECK_PALETTE", ""), PALETTES["pine"])

    TWICE_PEACH = "#ffb59e"
    TWICE_PINK = "#ff5aa8"
    TWICE_GLOW = "#ff8cc4"

    STATUS_OK = "#4ade80"
    STATUS_WARN = "#fde047"

    SIZE_HEADLINE = 30
    SIZE_BODY = 24
    SIZE_LIST = 22
    SIZE_CAPTION = 16

    def T(text, size=28, color=None, weight=None, font=None, **kwargs):
        m = Text(
            text,
            font=font or FONT,
            font_size=96,
            color=color or PALETTE["body"],
            weight=weight or NORMAL,
            **kwargs,
        )
        m.scale(size / 96)
        m.set_stroke(width=1.0 * (size / 96))
        return m

    def make_byline():
        py_logo = SVGMobject("assets/python.svg")
        py_logo.set_fill(PALETTE["body"], opacity=1).set_stroke(width=0)
        py_logo.set(height=0.24)
        return VGroup(
            T("Cyra Locsin", size=18, color=PALETTE["body"]),
            py_logo,
            T("Python WA", size=18, color=PALETTE["body"]),
        ).arrange(RIGHT, buff=0.14)

    def factoid(text, tilt=-1.5):
        content = text.upper()
        letters = T(content, size=20, color="#ede9e2")
        tape_color = ManimColor(PALETTE["accent"]).interpolate(
            ManimColor("#000000"), 0.72
        )
        depth = letters.copy()
        depth.set_color(tape_color.interpolate(ManimColor("#000000"), 0.5))
        depth.set_opacity(0.4)
        depth.shift(DOWN * 0.014)
        tape = RoundedRectangle(
            corner_radius=0.04,
            width=letters.width + 0.7, height=letters.height + 0.42,
            stroke_color="#4a4a48", stroke_width=1,
            fill_color=tape_color, fill_opacity=1,
        )
        depth.move_to(tape).shift(DOWN * 0.014)
        letters.move_to(tape)
        strip = VGroup(tape, depth, letters).rotate(tilt * DEGREES)
        strip.to_edge(DOWN, buff=0.35)
        return strip

    def box(label, sub=None, w=2.6, h=1.0, color=None, size=22):
        color = color or PALETTE["accent"]
        rect = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                                 stroke_color=color, stroke_width=2, fill_opacity=0)
        lab = T(label, size=size, color=PALETTE["title"], weight=BOLD)
        if sub:
            sub_t = T(sub, size=max(size - 8, 12), color=PALETTE["body"])
            VGroup(lab, sub_t).arrange(DOWN, buff=0.1).move_to(rect)
            return VGroup(rect, lab, sub_t)
        lab.move_to(rect)
        return VGroup(rect, lab)

    def arrow(a, b, color=None, sw=3, buff=0.12):
        return Arrow(a, b, color=color or PALETTE["accent"], stroke_width=sw,
                      buff=buff, max_tip_length_to_length_ratio=0.15)

    DIAGRAM_FILL_NORMAL = ManimColor(PALETTE["bg"]).interpolate(ManimColor(PALETTE["title"]), 0.14)
    DIAGRAM_FILL_LOW = ManimColor(PALETTE["bg"]).interpolate(ManimColor(PALETTE["accent"]), 0.45)

    def diagram_blk(label, dark=False, w=None, h=None, size=13, pad=0.16, rotate=False):
        txt = T(label, size=size, color=PALETTE["title"], line_spacing=0.85)
        if rotate:
            txt.rotate(PI / 2)
        bw = max(w, txt.width + pad) if w is not None else txt.width + pad
        bh = max(h, txt.height + pad) if h is not None else txt.height + pad
        rect = RoundedRectangle(corner_radius=0.06, width=bw, height=bh,
                                 stroke_color=PALETTE["body"], stroke_width=1,
                                 fill_color=DIAGRAM_FILL_LOW if dark else DIAGRAM_FILL_NORMAL,
                                 fill_opacity=1)
        txt.move_to(rect)
        return VGroup(rect, txt)

    def diagram_col(items, size=13, buff=0.08, rotate=False):
        txts = []
        for lbl, _ in items:
            t = T(lbl, size=size, line_spacing=0.85)
            if rotate:
                t.rotate(PI / 2)
            txts.append(t)
        w = max(t.width for t in txts) + 0.2
        boxes = [diagram_blk(lbl, dark=d, w=w, size=size, rotate=rotate) for lbl, d in items]
        return VGroup(*boxes).arrange(DOWN, buff=buff)

    def diagram_frame(title, body, pad=0.18, title_size=16, gap=0.12):
        hdr = T(title, size=title_size, color=PALETTE["title"], weight=BOLD)
        w = max(hdr.width, body.width) + pad * 2
        h = hdr.height + gap + body.height + pad * 2
        rect = RoundedRectangle(corner_radius=0.08, width=w, height=h,
                                 stroke_color=PALETTE["accent"], stroke_width=1.5,
                                 fill_opacity=0)
        group = VGroup(rect, hdr, body)
        hdr.move_to(rect.get_top() + DOWN * (pad + hdr.height / 2))
        body.move_to(rect.get_bottom() + UP * (pad + body.height / 2))
        return group

    def hex_row(byte_labels, color=None, cell=0.56, size=16):
        color = color or PALETTE["accent"]
        cells = VGroup()
        for b in byte_labels:
            sq = RoundedRectangle(corner_radius=0.06, width=cell, height=cell,
                                   stroke_color=color, stroke_width=1.5,
                                   fill_color=color, fill_opacity=0.1)
            lab = T(b, size=size, color=PALETTE["title"])
            lab.move_to(sq)
            cells.add(VGroup(sq, lab))
        cells.arrange(RIGHT, buff=0.1)
        return cells

    def brace_lab(mobj, text, color=None, direction=DOWN):
        color = color or PALETTE["accent"]
        b = Brace(mobj, direction, color=color, buff=0.1)
        lab = T(text, size=SIZE_CAPTION, color=color)
        b.put_at_tip(lab)
        return VGroup(b, lab)

    def stamp_verdict(label, reason, color):
        fill_color = ManimColor(color).interpolate(ManimColor("#000000"), 0.75)
        label_text = T(label, size=34, color=color, weight=BOLD)
        reason_text = T("reason: " + reason, size=16, color=color)
        inner = VGroup(label_text, reason_text).arrange(DOWN, buff=0.18)
        border = RoundedRectangle(corner_radius=0.08,
                                   width=inner.width + 0.9, height=inner.height + 0.7,
                                   stroke_color=color, stroke_width=5,
                                   fill_color=fill_color, fill_opacity=0.96)
        border.move_to(inner)
        return VGroup(border, inner).rotate(-8 * DEGREES)

    def axes_waveform(width=6.4, height=2.2, y_range=(-1.3, 1.3), x_range=(0, 10, 2)):
        return Axes(
            x_range=list(x_range), y_range=[y_range[0], y_range[1], 1],
            x_length=width, y_length=height,
            axis_config={"color": PALETTE["body"], "stroke_width": 1.5},
            tips=False,
        )

    def subcarrier_bars(n=12, width=4.8, height=1.8, color=None):
        color = color or PALETTE["accent"]
        bars = VGroup()
        for i in range(n):
            h = height * (0.28 + 0.68 * abs(np.sin(i * 1.7 + 0.4)))
            bar = RoundedRectangle(corner_radius=0.03, width=width / n * 0.65,
                                    height=h, fill_color=color, fill_opacity=0.75,
                                    stroke_width=0)
            bars.add(bar)
        bars.arrange(RIGHT, buff=width / n * 0.35, aligned_edge=DOWN)
        return bars

    def crowd_grid(rows=10, cols=16, spacing=0.36):
        dots = VGroup()
        info = []
        for r in range(rows):
            for c in range(cols):
                x = (c - (cols - 1) / 2) * spacing
                y = (r - (rows - 1) / 2) * spacing
                d = Dot(point=[x, y, 0], radius=spacing * 0.34,
                        color=PALETTE["body"], fill_opacity=0.22)
                dots.add(d)
                info.append((x, y))
        return dots, info

    def in_twice_logo(x, y, scale=1.7, a=1.25):
        x, y = x / scale, y / scale
        return (x**2 + y**2) ** 2 - a**2 * (x**2 - y**2) < 0

    def grad(alpha):
        return ManimColor(TWICE_PEACH).interpolate(ManimColor(TWICE_PINK), alpha)

    def icon_wifi(color=None, size=0.5):
        color = color or PALETTE["accent"]
        arcs = VGroup(*[
            Arc(radius=size * f, start_angle=PI / 2 - PI / 3.2, angle=PI / 1.6,
                color=color, stroke_width=3)
            for f in (0.4, 0.7, 1.0)
        ])
        dot = Dot(radius=size * 0.09, color=color, fill_opacity=1)
        return VGroup(arcs, dot)

    def icon_radar(color=None, size=0.5):
        color = color or PALETTE["accent"]
        dish = Circle(radius=size, color=color, stroke_width=2, stroke_opacity=0.6)
        sweep = Sector(radius=size, angle=PI / 5, color=color,
                        fill_opacity=0.4, stroke_width=0)
        sweep.rotate(50 * DEGREES, about_point=ORIGIN)
        center = Dot(radius=size * 0.07, color=color, fill_opacity=1)
        return VGroup(dish, sweep, center)

    def icon_twice_logo(color=None, size=0.5):
        color = color or TWICE_PINK
        a = size * 1.15
        return ParametricFunction(
            lambda t: np.array([
                a * np.cos(t) / (1 + np.sin(t) ** 2),
                a * np.sin(t) * np.cos(t) / (1 + np.sin(t) ** 2),
                0,
            ]),
            t_range=[0, TAU],
            color=color,
            stroke_width=3,
        )

    def icon_stick(color=None, size=0.5):
        color = color or TWICE_PINK
        head = Circle(radius=size * 0.32, color=color, fill_color=color,
                       fill_opacity=0.85, stroke_width=2)
        handle = RoundedRectangle(corner_radius=0.05, width=size * 0.22,
                                   height=size * 0.9, fill_color=PALETTE["body"],
                                   fill_opacity=0.15, stroke_color=color,
                                   stroke_width=2)
        handle.next_to(head, DOWN, buff=0)
        return VGroup(head, handle)

    class Count(Animation):
        def __init__(self, number, start, end, **kwargs):
            super().__init__(number, **kwargs)
            self.start_value = start
            self.end_value = end

        def interpolate_mobject(self, alpha):
            value = self.start_value + self.rate_func(alpha) * (
                self.end_value - self.start_value
            )
            self.mobject.set_value(value)


@app.class_definition
class Deck(Slide):
    def construct(self):
        self.camera.background_color = ManimColor(PALETTE["bg"])
        Text.set_default(stroke_width=1.0)

        self._title()
        self._me()
        self._three_inputs()
        self._micropython()
        self._boards()
        self._wifi()
        self._radar()
        self._lightsticks()
        self._close()


    def section_header(self, label, color=None, badge=None):
        heading = T(label, size=40, color=color or PALETTE["title"], weight=BOLD)
        heading.to_edge(UP, buff=0.6).to_edge(LEFT, buff=0.9)
        anchor = Line(LEFT * 7, RIGHT * 7).set_opacity(0)
        anchor.move_to(heading, coor_mask=[0, 1, 0])
        group = VGroup(heading, anchor)
        anims = [FadeIn(heading, shift=UP * 0.2)]
        if badge is not None:
            badge.set(height=0.55)
            badge.next_to(heading, RIGHT, buff=0.5)
            group.add(badge)
            anims.append(FadeIn(badge, scale=0.7))
        self.play(*anims, run_time=0.6)
        return group

    def place_body(self, mobj, hdr, bottom_buff=0.6):
        top = hdr.get_bottom()[1] - 0.3
        bottom = -config.frame_height / 2 + bottom_buff
        mobj.move_to([0, (top + bottom) / 2, 0])
        return mobj

    def clear_instantly(self, *mobs):
        self.remove(*[m for mob in mobs for m in mob.get_family()])

    def stamp_in(self, mob, color):
        self.play(FadeIn(mob, scale=1.6), run_time=0.25, rate_func=rush_into)
        self.play(Flash(mob, color=color, flash_radius=mob.width * 0.55,
                         num_lines=10, run_time=0.35))

    def rename_header(self, hdr, new_label, color=None):
        old = hdr[0]
        new = T(new_label, size=40, color=color or PALETTE["title"], weight=BOLD)
        new.move_to(old, aligned_edge=LEFT)
        self.play(TransformMatchingShapes(old, new), run_time=0.9)
        hdr.remove(old)
        hdr.add(new)


    def _title(self):
        self.next_slide()
        title_main = T("Tiny Snakes On A Board", size=60, color=PALETTE["title"],
                        weight=BOLD)
        title_main.set_stroke(width=1.8)
        title_main.shift(UP * 0.3)
        self.play(AddTextLetterByLetter(title_main), run_time=1.7)
        self.wait(0.2)

        underline = Line(
            title_main.get_left() + DOWN * 0.4, title_main.get_left() + DOWN * 0.4,
            color=PALETTE["accent"], stroke_width=3,
        )
        self.play(
            underline.animate.put_start_and_end_on(
                title_main.get_left() + DOWN * 0.4,
                title_main.get_right() + DOWN * 0.4,
            ),
            run_time=1, rate_func=smooth,
        )

        byline = make_byline()
        byline.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(byline), run_time=0.4)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeOut(title_main), FadeOut(underline), FadeOut(byline), run_time=0.6)


    def _me(self):
        hdr = self.section_header("Cyra Locsin")
        bullets = [
            "platform engineer, mainframes",
            "tinkerer"
        ]
        bullet_mobs = VGroup(*[T("· " + b, size=SIZE_LIST, color=PALETTE["body"])
                                for b in bullets])
        bullet_mobs.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        self.place_body(bullet_mobs, hdr)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in bullet_mobs],
                               lag_ratio=0.15, run_time=1.0))
        fact = factoid("mainframes can run Python code")
        self.play(FadeIn(fact, shift=UP * 0.15), run_time=0.4)
        self.next_slide()
        self.play(FadeOut(hdr), FadeOut(bullet_mobs), FadeOut(fact), run_time=0.6)


    def _three_inputs(self):
        hdr = self.section_header("Questionable Inputs")

        agenda = [
            (None, "MicroPython", "Python on Microcontrollers, no compiler"),
            (None, "ESP32", "the chip everything else in this talk runs on"),
            (icon_wifi, "Wi-Fi", "WIFI used as a motion sensor"),
            (icon_radar, "Radar", "a doppler radar chip that decodes a hand gesture"),
            (icon_stick, "K-pop merch", "reverse-engineering how concert lightsticks sync"),
        ]
        rows = VGroup()
        for icon_fn, label, desc in agenda:
            marker = icon_fn(size=0.35) if icon_fn else Dot(
                radius=0.16, color=PALETTE["accent"], fill_opacity=1)
            row = VGroup(marker, T(label, size=24, color=PALETTE["title"], weight=BOLD),
                         T(desc, size=SIZE_LIST, color=PALETTE["body"])).arrange(RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        self.place_body(rows, hdr)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rows],
                               lag_ratio=0.2, run_time=1.6))
        self.next_slide()
        self.rename_header(hdr, "Quite Interesting")
        self.next_slide()
        self.play(FadeOut(hdr), FadeOut(rows), run_time=0.6)


    def _boards(self):
        hdr = self.section_header("ESP32S3")

        def build_cpu_memory():
            left_col = diagram_col([("Cache", False), ("JTAG", False)])
            mid_col = diagram_col([("SRAM", False), ("ROM", False)])
            interrupt = diagram_blk("Interrupt\nMatrix", h=max(left_col.height, mid_col.height))
            row = VGroup(left_col, mid_col, interrupt).arrange(RIGHT, buff=0.2)
            cpu = diagram_blk("Xtensa® Dual-core 32-bit LX7\nMicroprocessor", w=row.width)
            body = VGroup(cpu, row).arrange(DOWN, buff=0.2)
            return diagram_frame("CPU and Memory", body)

        def build_rf():
            strip_labels = ["2.4 GHz\nReceiver", "2.4 GHz\nTransmitter", "RF\nSynthesizer"]
            measures = []
            for lbl in strip_labels:
                t = T(lbl, size=13, line_spacing=0.85)
                t.rotate(PI / 2)
                measures.append(t)
            strip_w = max(t.width for t in measures) + 0.16
            strips = VGroup(*[diagram_blk(lbl, rotate=True, w=strip_w) for lbl in strip_labels])
            strips.arrange(RIGHT, buff=0.1, aligned_edge=UP)
            top = diagram_blk("2.4 GHz Balun +\nSwitch", w=strips.width)
            left = VGroup(top, strips).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            right = diagram_col([
                ("External Main\nClock", False),
                ("Fast RC\nOscillator", False),
                ("Phase Lock\nLoop", False),
            ])
            body = VGroup(left, right).arrange(RIGHT, buff=0.25, aligned_edge=UP)
            return diagram_frame("RF", body)

        def build_wireless():
            mac_txt = T("Wi-Fi MAC", size=13, line_spacing=0.85)
            bb_txt = T("Wi-Fi\nBaseband", size=13, line_spacing=0.85)
            h = max(mac_txt.height, bb_txt.height) + 0.16
            w = max(mac_txt.width, bb_txt.width) + 0.16
            wifi_mac = diagram_blk("Wi-Fi MAC", w=w, h=h)
            wifi_bb = diagram_blk("Wi-Fi\nBaseband", w=w, h=h)
            row1 = VGroup(wifi_mac, wifi_bb).arrange(RIGHT, buff=0.16)
            bt_lc = diagram_blk("Bluetooth LE Link Controller", w=row1.width)
            bt_bb = diagram_blk("Bluetooth LE Baseband", w=row1.width)
            body = VGroup(row1, bt_lc, bt_bb).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            return diagram_frame("Wireless Digital Circuits", body)

        def build_peripherals():
            col1 = diagram_col([("GDMA", False), ("SD/MMC\nHost", False), ("SPI0/1", False),
                                 ("USB OTG", False), ("UART", False), ("RMT", False)])
            col2 = diagram_col([("System\nTimer", False), ("Pulse\nCounter", False), ("SPI2/3", False),
                                 ("TWAI®", False), ("LED PWM", False), ("LCD\nInterface", False)])
            col3 = diagram_col([("General-\npurpose\nTimers", False), ("World\nController", False),
                                 ("I2S", False), ("I2C", False), ("MCPWM", False),
                                 ("Camera\nInterface", False)])
            col4 = diagram_col([("GPIO", False), ("DIG ADC", False), ("USB Serial/\nJTAG", False),
                                 ("Main System\nWatchdog\nTimers", False), ("Super\nWatchdog", True),
                                 ("RTC I2C", True)])
            col5 = diagram_col([("RTC GPIO", True), ("RTC ADC", True), ("eFuse\nController", True),
                                 ("RTC\nWatchdog\nTimer", True), ("Touch\nSensor", True),
                                 ("Temperature\nSensor", True)])
            body = VGroup(col1, col2, col3, col4, col5).arrange(RIGHT, buff=0.18, aligned_edge=UP)
            return diagram_frame("Peripherals", body)

        def build_security():
            labels = ["SHA", "RSA", "AES", "RNG"]
            txts = [T(lbl, size=13) for lbl in labels]
            s = max(max(t.width for t in txts), max(t.height for t in txts)) + 0.16
            top_row = VGroup(*[diagram_blk(lbl, w=s, h=s) for lbl in labels]).arrange(RIGHT, buff=0.1)
            left_col = diagram_col([
                ("HMAC", False), ("Secure Boot", False), ("Permission\nControl", False),
            ])
            right_col = diagram_col([("RSA_DS", False), ("Flash\nEncryption", False)])
            cols_row = VGroup(left_col, right_col).arrange(RIGHT, buff=0.1, aligned_edge=UP)
            body = VGroup(top_row, cols_row).arrange(DOWN, buff=0.16)
            return diagram_frame("Security", body)

        def build_rtc():
            h = max(diagram_blk("RTC\nMemory", dark=True).height, diagram_blk("PMU", dark=True).height)
            rtc_mem = diagram_blk("RTC\nMemory", dark=True, h=h)
            pmu = diagram_blk("PMU", dark=True, h=h)
            row = VGroup(rtc_mem, pmu).arrange(RIGHT, buff=0.16)
            ulp = diagram_blk("ULP Coprocessor", dark=True, w=row.width)
            body = VGroup(row, ulp).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            return diagram_frame("RTC", body)

        def build_legend():
            label = T("Power consumption", size=14, color=PALETTE["title"], weight=BOLD)
            normal_swatch = RoundedRectangle(width=0.7, height=0.28, corner_radius=0.14,
                                              stroke_color=PALETTE["body"], stroke_width=1,
                                              fill_color=DIAGRAM_FILL_NORMAL, fill_opacity=1)
            normal_row = VGroup(normal_swatch, T("Normal", size=12, color=PALETTE["body"])
                                 ).arrange(RIGHT, buff=0.18)
            low_swatch = RoundedRectangle(width=0.7, height=0.28, corner_radius=0.14,
                                           stroke_color=PALETTE["body"], stroke_width=1,
                                           fill_color=DIAGRAM_FILL_LOW, fill_opacity=1)
            low_row = VGroup(low_swatch,
                              T("Low power / deep-sleep capable", size=12, color=PALETTE["body"])
                              ).arrange(RIGHT, buff=0.18)
            rows = VGroup(normal_row, low_row).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            return VGroup(label, rows).arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        cpu_mem = build_cpu_memory()
        rf = build_rf()
        wireless = build_wireless()
        peripherals = build_peripherals()
        security = build_security()
        rtc = build_rtc()

        row1 = VGroup(cpu_mem, rf, wireless).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        security_rtc = VGroup(security, rtc).arrange(DOWN, buff=0.22)
        row2 = VGroup(peripherals, security_rtc).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        panel_body = VGroup(row1, row2).arrange(DOWN, buff=0.28)
        outer = diagram_frame("Espressif ESP32-S3 Wi-Fi + Bluetooth® Low Energy SoC",
                               panel_body, title_size=20, pad=0.3)
        legend = build_legend()
        diagram = VGroup(outer, legend).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        top = hdr.get_bottom()[1] - 0.3
        bottom = -config.frame_height / 2 + 0.6
        if diagram.width > config.frame_width - 0.6:
            diagram.scale_to_fit_width(config.frame_width - 0.6)
        if diagram.height > top - bottom:
            diagram.scale_to_fit_height(top - bottom)
        self.place_body(diagram, hdr)

        self.play(FadeIn(outer[0]), FadeIn(outer[1]), run_time=0.4)
        self.play(LaggedStart(FadeIn(cpu_mem), FadeIn(rf), FadeIn(wireless),
                               FadeIn(peripherals), FadeIn(security), FadeIn(rtc),
                               lag_ratio=0.15, run_time=1.5))
        self.play(FadeIn(legend), run_time=0.4)
        self.next_slide()
        self.play(FadeOut(hdr), FadeOut(diagram), run_time=0.5)


    def _micropython(self):
        hdr = self.section_header("MicroPython")

        mp_line = T("Damien George, 2013 Kickstarter", size=SIZE_BODY,
                     color=PALETTE["body"])
        prefix = T("£", size=44, color=PALETTE["title"])
        amount = DecimalNumber(15000, num_decimal_places=0, color=PALETTE["title"],
                                font_size=64)
        amount.next_to(prefix, RIGHT, buff=0.1)
        money = VGroup(prefix, amount)
        stack = VGroup(mp_line, money).arrange(DOWN, buff=0.6)
        self.place_body(stack, hdr)
        amount.add_updater(lambda m: m.next_to(prefix, RIGHT, buff=0.1))
        self.play(FadeIn(mp_line, shift=UP * 0.2), FadeIn(money), run_time=0.6)
        self.next_slide()
        self.play(Count(amount, 15000, 100000, run_time=2.2, rate_func=smooth))
        self.add_sound("assets/audio/chime.wav")
        self.play(Indicate(amount, color=PALETTE["accent"], scale_factor=1.15))
        self.next_slide()
        amount.clear_updaters()
        self.play(FadeOut(mp_line), money.animate.scale(1.4).set_opacity(0), run_time=0.6)

        features_title = T("Key features:", size=SIZE_HEADLINE, color=PALETTE["title"],
                            weight=BOLD)
        feature_strs = [
            "REPL — poke the hardware live",
            "No compile step — save, it runs",
            "asyncio built in — cooperative concurrency",
            "CPython-like syntax — muscle memory transfers",
        ]
        feature_mobs = VGroup(*[T("· " + f, size=SIZE_LIST, color=PALETTE["body"])
                                 for f in feature_strs])
        feature_mobs.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        features = VGroup(features_title, feature_mobs).arrange(DOWN, buff=0.5,
                                                                  aligned_edge=LEFT)
        self.place_body(features, hdr)
        self.play(FadeIn(features_title, shift=UP * 0.2), run_time=0.4)
        self.next_slide()
        self.play(FadeIn(feature_mobs[0], shift=LEFT * 0.2), run_time=0.35)
        self.next_slide()
        self.play(FadeIn(feature_mobs[1], shift=LEFT * 0.2), run_time=0.35)
        self.next_slide()
        self.play(FadeIn(feature_mobs[2], shift=LEFT * 0.2), run_time=0.35)
        self.next_slide()
        self.play(FadeIn(feature_mobs[3], shift=LEFT * 0.2), run_time=0.35)
        self.next_slide()
        self.play(FadeOut(features), run_time=0.5)

        trad_label = T("Arduino IDE — C++", size=SIZE_CAPTION, color=PALETTE["body"])
        trad_boxes = VGroup(*[box(s, w=2.1, h=0.9, size=18)
                               for s in ["Write C++", "Compile", "Flash", "Runs"]])
        trad_boxes.arrange(RIGHT, buff=0.55)
        trad_arrows = VGroup(*[
            arrow(trad_boxes[i].get_right(), trad_boxes[i + 1].get_left())
            for i in range(len(trad_boxes) - 1)
        ])
        trad_loop = CurvedArrow(trad_boxes[-1].get_bottom(), trad_boxes[0].get_bottom(),
                                 angle=TAU / 4, color=PALETTE["body"], stroke_width=2)
        trad_row = VGroup(trad_boxes, trad_arrows, trad_loop)
        trad_label.next_to(trad_row, UP, buff=0.3).align_to(trad_row, LEFT)

        mp_label = T("MicroPython — REPL", size=SIZE_CAPTION, color=PALETTE["accent"])
        mp_boxes = VGroup(*[box(s, w=2.1, h=0.9, size=18, color=PALETTE["accent"])
                             for s in ["Read", "Eval", "Print", "Loop"]])
        mp_boxes.arrange(RIGHT, buff=0.55)
        mp_arrows = VGroup(*[
            arrow(mp_boxes[i].get_right(), mp_boxes[i + 1].get_left(), color=PALETTE["accent"])
            for i in range(len(mp_boxes) - 1)
        ])
        mp_loop = CurvedArrow(mp_boxes[-1].get_bottom(), mp_boxes[0].get_bottom(),
                               angle=TAU / 4, color=PALETTE["accent"], stroke_width=2)
        mp_row = VGroup(mp_boxes, mp_arrows, mp_loop)
        mp_label.next_to(mp_row, UP, buff=0.3).align_to(mp_row, LEFT)

        content = VGroup(
            VGroup(trad_label, trad_row), VGroup(mp_label, mp_row),
        ).arrange(DOWN, buff=1.1, aligned_edge=LEFT)
        self.place_body(content, hdr)

        self.play(FadeIn(trad_label, shift=UP * 0.15), run_time=0.4)
        self.play(Succession(
            FadeIn(trad_boxes[0], run_time=0.5, rate_func=ease_out_expo),
            Create(trad_arrows[0], run_time=0.4),
            FadeIn(trad_boxes[1], run_time=0.6, rate_func=ease_out_expo),
            Create(trad_arrows[1], run_time=0.4),
            FadeIn(trad_boxes[2], run_time=0.6, rate_func=ease_out_expo),
            Create(trad_arrows[2], run_time=0.4),
            FadeIn(trad_boxes[3], run_time=0.6, rate_func=ease_out_expo),
            Create(trad_loop, run_time=0.6),
        ))
        self.next_slide()

        self.play(FadeIn(mp_label, shift=UP * 0.15), run_time=0.3)
        self.play(LaggedStart(
            FadeIn(mp_boxes[0]), Create(mp_arrows[0]),
            FadeIn(mp_boxes[1]), Create(mp_arrows[1]),
            FadeIn(mp_boxes[2]), Create(mp_arrows[2]),
            FadeIn(mp_boxes[3]), Create(mp_loop),
            lag_ratio=0.12, run_time=0.7, rate_func=ease_out_expo,
        ))
        self.next_slide()
        self.play(FadeOut(trad_label), FadeOut(trad_row),
                  FadeOut(mp_label), FadeOut(mp_row), run_time=0.5)

        board_w, board_h = 8.4, 2.2
        board = RoundedRectangle(corner_radius=0.1, width=board_w, height=board_h,
                                  stroke_color=PALETTE["body"], stroke_width=2,
                                  fill_color=PALETTE["bg"], fill_opacity=1)
        hole_xs = np.linspace(-board_w / 2 + 0.6, board_w / 2 - 0.6, 14)
        holes = VGroup(*[
            Dot([x, y, 0], radius=0.03, color=PALETTE["body"], fill_opacity=0.35)
            for y in (0.65, -0.65)
            for x in hole_xs
        ])
        breadboard = VGroup(board, holes)
        self.place_body(breadboard, hdr)
        self.play(FadeIn(breadboard), run_time=0.5)

        by = board.get_y()

        def legs(col, color=None, gap=0.0):
            x = hole_xs[col]
            color = color or PALETTE["body"]
            top = Line([x, 0.65 + by, 0], [x, gap + by, 0], color=color, stroke_width=3)
            bot = Line([x, -gap + by, 0], [x, -0.65 + by, 0], color=color, stroke_width=3)
            return top, bot

        caption = T("Connect one thing —", size=SIZE_BODY, color=PALETTE["body"])
        caption.next_to(breadboard, DOWN, buff=0.5)
        disclaimer = T("(not an exact approximation of real components)",
                        size=SIZE_CAPTION, color=PALETTE["body"])
        disclaimer.next_to(caption, DOWN, buff=0.3)
        self.play(FadeIn(caption, shift=UP * 0.15), FadeIn(disclaimer), run_time=0.4)

        wire_top, wire_bot = legs(2, color="#e0574e")
        wire = VGroup(wire_top, wire_bot)
        self.play(Create(wire), run_time=0.5)
        self.next_slide()

        new_caption = T("see if it does anything —", size=SIZE_BODY, color=PALETTE["body"])
        new_caption.move_to(caption)
        self.play(FadeOut(caption), FadeIn(new_caption, shift=UP * 0.1), run_time=0.4)
        caption = new_caption
        self.play(Flash(wire, color=PALETTE["accent"], flash_radius=0.35), run_time=0.4)
        self.next_slide()

        new_caption = T("connect another —", size=SIZE_BODY, color=PALETTE["body"])
        new_caption.move_to(caption)
        self.play(FadeOut(caption), FadeIn(new_caption, shift=UP * 0.1), run_time=0.4)
        caption = new_caption

        r_col = 6
        r_x = hole_xs[r_col]
        r_top, r_bot = legs(r_col, gap=0.22)
        r_body = VMobject(stroke_color="#c9a35c", stroke_width=4)
        r_body.set_points_as_corners([
            [r_x, 0.22 + by, 0], [r_x + 0.12, 0.13 + by, 0], [r_x - 0.12, -0.04 + by, 0],
            [r_x + 0.12, -0.13 + by, 0], [r_x, -0.22 + by, 0],
        ])
        resistor = VGroup(r_top, r_body, r_bot)
        self.play(Create(resistor), run_time=0.6)
        self.next_slide()

        new_caption = T("...and run out of breadboard.", size=SIZE_BODY, color=PALETTE["body"])
        new_caption.move_to(caption)
        self.play(FadeOut(caption), FadeIn(new_caption, shift=UP * 0.1), run_time=0.4)
        caption = new_caption

        led_col1, led_col2 = 9, 10
        led_x1, led_x2 = hole_xs[led_col1], hole_xs[led_col2]
        led_leg1 = Line([led_x1, 0.95 + by, 0], [led_x1, 0.65 + by, 0],
                         color=PALETTE["body"], stroke_width=3)
        led_leg2 = Line([led_x2, 0.95 + by, 0], [led_x2, 0.65 + by, 0],
                         color=PALETTE["body"], stroke_width=3)
        led_bulb = Circle(radius=0.3, stroke_color=PALETTE["body"], stroke_width=2,
                           fill_color=PALETTE["accent"], fill_opacity=0.12)
        led_bulb.move_to([(led_x1 + led_x2) / 2, 1.25 + by, 0])
        led = VGroup(led_leg1, led_leg2, led_bulb)
        self.play(Create(led_leg1), Create(led_leg2),
                  FadeIn(led_bulb, scale=0.7, rate_func=ease_out_expo), run_time=0.6)

        top_rail = Line([hole_xs[2], 0.65 + by, 0], [hole_xs[led_col1], 0.65 + by, 0],
                         color=PALETTE["body"], stroke_width=2)
        bottom_rail = Line([hole_xs[2], -0.65 + by, 0], [hole_xs[r_col], -0.65 + by, 0],
                            color=PALETTE["body"], stroke_width=2)
        rails = VGroup(top_rail, bottom_rail)
        self.play(Create(rails), run_time=0.5)
        self.next_slide()

        new_caption = T("Test it via the REPL.", size=SIZE_BODY, color=PALETTE["accent"])
        new_caption.move_to(caption)
        repl_box = box("REPL", ">>> led.on()", w=2.6, h=1.0)
        repl_box.next_to(led, RIGHT, buff=0.8)
        repl_arrow = arrow(repl_box.get_left(), led_bulb.get_right() + RIGHT * 0.1)
        self.play(Succession(
            AnimationGroup(FadeOut(caption), FadeIn(new_caption, shift=UP * 0.1), run_time=0.4),
            AnimationGroup(FadeIn(repl_box, shift=LEFT * 0.2), Create(repl_arrow), run_time=0.5),
            led_bulb.animate(run_time=0.3, rate_func=ease_out_expo).set_fill(opacity=1),
            Flash(led_bulb, color=PALETTE["accent"], flash_radius=0.5, run_time=0.4),
        ))
        self.add_sound("assets/audio/beep.wav")
        workflow = VGroup(breadboard, new_caption, disclaimer, wire, resistor, led,
                           rails, repl_box, repl_arrow)
        self.next_slide()
        self.play(FadeOut(workflow), run_time=0.5)

        wokwi = T("Wokwi — break a virtual board in the browser first.", size=SIZE_HEADLINE,
                   color=PALETTE["accent"])
        wokwi_img = ImageMobject("assets/wokwi_screenshot.png")
        wokwi_img.set(width=9.5)
        wokwi_border = RoundedRectangle(corner_radius=0.04, width=wokwi_img.width + 0.06,
                                         height=wokwi_img.height + 0.06,
                                         stroke_color=PALETTE["accent"], stroke_width=2,
                                         fill_opacity=0)
        wokwi_border.move_to(wokwi_img)
        wokwi_shot = Group(wokwi_img, wokwi_border)
        wokwi_shot.next_to(wokwi, DOWN, buff=0.4)
        self.place_body(Group(wokwi, wokwi_shot), hdr)
        self.play(FadeIn(wokwi, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(wokwi_shot, shift=UP * 0.15), run_time=0.5)
        self.next_slide()
        self.play(FadeOut(hdr), FadeOut(wokwi), FadeOut(wokwi_shot), run_time=0.6)

        space_fact = factoid("space agencies fly MicroPython — remote reflash "
                              "beats a physical visit")
        self.play(FadeIn(space_fact, shift=UP * 0.15), run_time=0.4)
        self.next_slide()
        self.play(FadeOut(space_fact), run_time=0.4)


    def _wifi(self):
        hdr = self.section_header("QI: Wifi CSI", badge=icon_wifi())
        self.rename_header(hdr, "Wifi CSI")

        curdle = T("curdle.sh — terminal Wordle, DICT protocol\n"
                    "instead of a local dictionary.", size=SIZE_BODY, color=PALETTE["body"])
        self.place_body(curdle, hdr)
        self.play(FadeIn(curdle, shift=UP * 0.2), run_time=0.5)
        self.next_slide()
        self.play(FadeOut(curdle), run_time=0.4)

        def tile(letter, state):
            color = {"hit": STATUS_OK, "near": STATUS_WARN}.get(state, PALETTE["body"])
            sq = RoundedRectangle(corner_radius=0.05, width=0.42, height=0.42,
                                   stroke_color=color, stroke_width=1.5,
                                   fill_color=color, fill_opacity=0.1 if state == "miss" else 0.4)
            lab = T(letter.upper(), size=18, color=PALETTE["title"], weight=BOLD)
            lab.move_to(sq)
            return VGroup(sq, lab)

        def tile_row(word, states):
            return VGroup(*[tile(c, s) for c, s in zip(word, states)]).arrange(RIGHT, buff=0.08)

        term = RoundedRectangle(corner_radius=0.15, width=9.6, height=4.6,
                                 stroke_color=PALETTE["accent"], stroke_width=2,
                                 fill_opacity=0)
        new_cmd = T("$ curl -L curdle.sh/new", size=20, color=PALETTE["body"],
                     t2c={"$": PALETTE["accent"]})
        link_out = T("curdle.sh/DB94Zg6k", size=20, color=PALETTE["accent"])
        guess1_cmd = T("$ curl -L curdle.sh/DB94Zg6k/crane", size=20,
                        color=PALETTE["body"], t2c={"$": PALETTE["accent"]})
        feedback1 = tile_row("crane", ["near", "hit", "hit", "miss", "hit"])
        guess2_cmd = T("$ curl -L curdle.sh/DB94Zg6k/trace", size=20,
                        color=PALETTE["body"], t2c={"$": PALETTE["accent"]})
        feedback2 = tile_row("trace", ["hit"] * 5)

        block = VGroup(new_cmd, link_out, guess1_cmd, feedback1, guess2_cmd, feedback2)
        block.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        block.move_to(term).align_to(term.get_left() + RIGHT * 0.4, LEFT)

        self.place_body(VGroup(term, block), hdr)
        self.play(FadeIn(term), run_time=0.4)
        self.play(AddTextLetterByLetter(new_cmd), run_time=1.0)
        self.next_slide()
        self.play(FadeIn(link_out, shift=UP * 0.1), run_time=0.4)
        self.next_slide()
        self.play(AddTextLetterByLetter(guess1_cmd), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(t, scale=1.3) for t in feedback1],
                               lag_ratio=0.15, run_time=0.8))
        self.next_slide()
        self.play(AddTextLetterByLetter(guess2_cmd), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(t, scale=1.3) for t in feedback2],
                               lag_ratio=0.15, run_time=0.8))
        self.next_slide()
        self.play(FadeOut(term), FadeOut(block), run_time=0.5)

        rssi_label = T("RSSI", size=30, color=PALETTE["title"], weight=BOLD)
        rssi_val = DecimalNumber(-62, num_decimal_places=0, color=PALETTE["accent"],
                                  font_size=72)
        rssi_unit = T("dBm", size=22, color=PALETTE["body"])
        rssi_row = VGroup(rssi_val, rssi_unit).arrange(RIGHT, buff=0.2)
        rssi_stack = VGroup(rssi_label, rssi_row).arrange(DOWN, buff=0.5)
        self.place_body(rssi_stack, hdr)
        self.play(FadeIn(rssi_label, shift=UP * 0.2), FadeIn(rssi_row), run_time=0.6)
        self.next_slide()

        csi_label = T("CSI", size=30, color=PALETTE["title"], weight=BOLD)
        csi_label.move_to(rssi_label)
        bars = subcarrier_bars(n=14, width=6.0, height=1.8, color=PALETTE["accent"])
        bars.next_to(csi_label, DOWN, buff=0.6)
        csi_note = T("amplitude + phase, per subcarrier", size=SIZE_CAPTION, color=PALETTE["body"])
        csi_note.next_to(bars, DOWN, buff=0.3)
        self.play(
            TransformMatchingShapes(rssi_label, csi_label),
            FadeOut(rssi_row, shift=DOWN * 0.2),
            LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.06, run_time=1.2),
            FadeIn(csi_note),
        )
        self.next_slide()
        self.play(FadeOut(csi_label), FadeOut(bars), FadeOut(csi_note), run_time=0.6)

        esp_a = box("ESP32", "sender", color=PALETTE["accent"], w=2.2, h=1.0)
        esp_a.to_edge(LEFT, buff=1.4)
        esp_b = box("ESP32", "receiver", color=PALETTE["accent"], w=2.2, h=1.0)
        esp_b.to_edge(RIGHT, buff=1.4)
        me_dot = Circle(radius=0.32, color=PALETTE["title"], fill_color=PALETTE["title"],
                         fill_opacity=0.15, stroke_width=2)
        me_label = T("me", size=18, color=PALETTE["title"])
        me_label.move_to(me_dot)
        me_group = VGroup(me_dot, me_label)
        me_group.move_to((esp_a.get_center() + esp_b.get_center()) / 2)
        clock = box("ESP32", "clock", color=PALETTE["body"], w=2.0, h=0.9)
        clock.next_to(me_group, UP, buff=1.0)
        a1 = arrow(esp_a.get_right(), me_dot.get_left())
        a2 = arrow(me_dot.get_right(), esp_b.get_left())
        self.place_body(VGroup(esp_a, esp_b, clock, me_group, a1, a2), hdr)
        self.play(FadeIn(esp_a), FadeIn(esp_b), FadeIn(clock), FadeIn(me_group),
                  Create(a1), Create(a2), run_time=0.6)
        ring = Circle(radius=0.15, color=PALETTE["accent"], stroke_width=3)
        ring.move_to(esp_a.get_right())
        self.play(Broadcast(ring, focal_point=esp_a.get_right(), n_mobs=3,
                             initial_width=0.15, run_time=1.6),
                  Flash(me_group, color=PALETTE["accent"], flash_radius=0.5))
        self.next_slide()
        self.play(FadeOut(esp_a), FadeOut(esp_b), FadeOut(clock), FadeOut(me_group),
                  FadeOut(a1), FadeOut(a2), FadeOut(ring), run_time=0.4)

        steps = ["hand", "arm", "whole body", "walking in and out of the room at 3am"]
        step_group = VGroup(*[T("· " + s, size=SIZE_LIST, color=PALETTE["body"]) for s in steps])
        step_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        self.place_body(step_group, hdr)
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.3) for s in step_group],
                               lag_ratio=0.3, run_time=1.6))
        self.next_slide()
        self.play(FadeOut(step_group), run_time=0.5)

        ax = axes_waveform(width=7.5, height=2.6, y_range=(-1.4, 1.4))
        signal = ax.plot(
            lambda x: 0.55 * np.sin(x * 1.3) + 0.25 * np.sin(x * 4.7 + 1)
            + 0.15 * np.sin(x * 11 + 2),
            color=PALETTE["accent"], x_range=[0, 10, 0.02],
        )
        caption = T("real captures — synthetic shape shown here", size=SIZE_CAPTION,
                     color=PALETTE["body"])
        caption.next_to(ax, DOWN, buff=0.25)
        self.place_body(VGroup(ax, signal, caption), hdr)
        self.play(Create(ax), run_time=0.5)
        self.play(Create(signal, run_time=1.6, rate_func=linear), FadeIn(caption))
        self.next_slide()

        fail = Cross(stroke_color=PALETTE["accent"], scale_factor=0.4)
        fail.move_to(signal.get_end())
        fail_note = T("no clean, repeatable data to classify", size=SIZE_BODY,
                       color=PALETTE["accent"])
        fail_note.next_to(ax, UP, buff=0.3)
        self.play(Create(fail), FadeIn(fail_note, shift=UP * 0.1), run_time=0.7)

        aside = factoid("fibre carries distributed acoustic sensing too")
        self.play(FadeIn(aside, shift=UP * 0.15), run_time=0.4)
        self.next_slide()
        deferred = stamp_verdict("DEFERRED", "needs an antenna array", STATUS_WARN)
        self.place_body(deferred, hdr)
        self.stamp_in(deferred, STATUS_WARN)
        self.next_slide()
        self.play(FadeOut(ax), FadeOut(signal), FadeOut(fail_note), FadeOut(caption),
                  FadeOut(aside), FadeOut(hdr), FadeOut(deferred),
                  ShrinkToCenter(fail), run_time=0.6)


    def _radar(self):
        hdr = self.section_header("QI: Doppler Radar", badge=icon_radar())
        self.play(Circumscribe(hdr, color=PALETTE["accent"], run_time=0.8))
        self.rename_header(hdr, "Doppler Radar")

        pivot = T("One ESP32. One sensor actually\nbuilt to detect motion.", size=SIZE_BODY,
                   color=PALETTE["body"])
        self.place_body(pivot, hdr)
        self.play(FadeIn(pivot, shift=UP * 0.2), run_time=0.5)
        self.next_slide()
        self.play(FadeOut(pivot), run_time=0.4)

        dish = icon_radar(size=0.9)
        dish.to_edge(LEFT, buff=1.8)
        doppler_label = T("CDM324 — 24 GHz, single-channel.\n"
                           "Transmit, reflect, frequency shifts with speed.",
                           size=SIZE_BODY, color=PALETTE["title"])
        doppler_label.to_edge(RIGHT, buff=1.4)
        target = Dot(radius=0.14, color=PALETTE["accent"], fill_opacity=1)
        target.move_to(dish.get_center() + RIGHT * 3.4)
        self.place_body(VGroup(dish, doppler_label, target), hdr)
        self.play(FadeIn(dish), FadeIn(doppler_label), FadeIn(target), run_time=0.5)

        pulse = Dot(radius=0.07, color=PALETTE["title"], fill_opacity=1)
        pulse.move_to(dish.get_center())
        tx_ring = Circle(radius=0.4, color=PALETTE["title"], stroke_width=2)
        tx_ring.move_to(dish.get_center())
        self.play(
            MoveAlongPath(pulse, Line(dish.get_center(), target.get_center())),
            Broadcast(tx_ring, focal_point=dish.get_center(), n_mobs=2,
                       initial_width=0.1, run_time=1.4),
            run_time=1.4, rate_func=linear,
        )

        self.play(Flash(target, color=PALETTE["accent"], flash_radius=0.3), run_time=0.3)
        pulse.set_color(PALETTE["accent"])
        rx_ring = Circle(radius=0.32, color=PALETTE["accent"], stroke_width=2)
        rx_ring.move_to(target.get_center())
        self.play(
            MoveAlongPath(pulse, Line(target.get_center(), dish.get_center() + RIGHT * 0.9)),
            Broadcast(rx_ring, focal_point=target.get_center(), n_mobs=3,
                       initial_width=0.08, run_time=1.2),
            target.animate.move_to(dish.get_center() + RIGHT * 0.9),
            run_time=1.2, rate_func=linear,
        )
        self.play(FadeOut(pulse), Flash(dish, color=PALETTE["accent"], flash_radius=0.5),
                   run_time=0.4)
        self.next_slide()
        self.play(FadeOut(dish), FadeOut(doppler_label), FadeOut(target), run_time=0.5)

        circuit_lines = VGroup(*[
            T(s, size=SIZE_BODY, color=PALETTE["body"]) for s in [
                "LM386 amp, caps from the drawer.",
                "CDM324 wants 5.5V — ESP32 only gives 3V3 logic and 5V.",
                "Fixed by soldering the IN/OUT pad for the raw IF output.",
            ]
        ]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        self.place_body(circuit_lines, hdr)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in circuit_lines],
                               lag_ratio=0.3, run_time=1.2))
        self.next_slide()
        self.play(FadeOut(circuit_lines), run_time=0.4)

        demo_title = T("On the board: morse-radar", size=SIZE_HEADLINE,
                        color=PALETTE["title"], weight=BOLD)
        demo_items = VGroup(*[
            T("· " + s, size=SIZE_LIST, color=PALETTE["body"]) for s in [
                "signal check — raw envelope, is it even moving",
                "speed readout — live km/h off the Doppler shift",
                "drill — screen times the gesture, tunes the thresholds",
                "decode — live Morse, still a bit lossy",
            ]
        ]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        demo = VGroup(demo_title, demo_items).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        self.place_body(demo, hdr)
        self.play(FadeIn(demo_title, shift=UP * 0.2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(i, shift=LEFT * 0.2) for i in demo_items],
                               lag_ratio=0.25, run_time=1.3))
        self.next_slide()
        wip = stamp_verdict("WORK IN PROGRESS", "BLE to macOS not paired yet", STATUS_WARN)
        wip.move_to(demo_items[-1]).shift(RIGHT * 1.0 + UP * 0.1)
        self.stamp_in(wip, STATUS_WARN)
        self.next_slide()
        self.clear_instantly(hdr, demo, wip)
        self.next_slide(
            src=Path("assets/demos/doppler_framed.mp4"),
        )
        self.next_slide()
        hdr = self.section_header("Doppler Radar", badge=icon_radar())
        self.next_slide()
        self.play(FadeOut(hdr), run_time=0.6)


    def _lightsticks(self):
        title = "Twice the Signals (BLE GATT & 447.9 MHz)"
        hdr = self.section_header("QI: " + title, color=TWICE_PINK, badge=icon_stick())
        self.rename_header(hdr, title, color=TWICE_PINK)

        logo = icon_twice_logo(size=0.9)
        setup_items = VGroup(*[
            T("· " + s, size=SIZE_LIST, color=PALETTE["body"]) for s in [
                "Twice concerts are the BEST",
                "I've flown to three TWICE concerts in Australia",
                "The crowd lightshows are AMAZING",
            ]
        ]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        setup_group = VGroup(logo, setup_items).arrange(DOWN, buff=0.5)
        self.place_body(setup_group, hdr)
        self.play(FadeIn(logo, scale=0.7), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(i, shift=LEFT * 0.2) for i in setup_items],
                               lag_ratio=0.3, run_time=1.3))
        self.next_slide()
        self.play(FadeOut(setup_group), run_time=0.4)

        v_header = ["stick", "radios", "protocol docs"]
        v_rows = [
            ("V1", "BLE 4.1 (app), crowd sync: unknown", "nothing published"),
            ("V3", "BLE (app) + sub-GHz venue link", "maximus64/candybong"),
        ]
        v_cells = VGroup()
        for label in v_header:
            v_cells.add(T(label, size=SIZE_CAPTION, color=TWICE_PINK, weight=BOLD))
        for stick, radios, docs in v_rows:
            v_cells.add(T(stick, size=SIZE_LIST, color=PALETTE["title"], weight=BOLD))
            v_cells.add(T(radios, size=SIZE_LIST, color=PALETTE["body"]))
            v_cells.add(T(docs, size=SIZE_LIST, color=TWICE_PEACH))
        v_cells.arrange_in_grid(rows=len(v_rows) + 1, cols=3, buff=(0.6, 0.3),
                                 col_alignments="lll")
        self.place_body(v_cells, hdr)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in v_cells],
                               lag_ratio=0.06, run_time=1.2))
        self.play(Indicate(VGroup(v_cells[5], v_cells[8]), color=TWICE_PEACH,
                            scale_factor=1.1))
        self.next_slide()
        self.play(FadeOut(v_cells), run_time=0.5)

        crowd_note = VGroup(*[
            T(s, size=SIZE_BODY, color=PALETTE["body"]) for s in [
                "IR wristbands → radio.",
                "BLE-for-app + separate venue radio.",
                "Devices mapped to seats.",
            ]
        ]).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        self.place_body(crowd_note, hdr)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in crowd_note],
                               lag_ratio=0.3, run_time=1.2))
        self.next_slide()
        self.play(FadeOut(crowd_note), run_time=0.4)

        crowdsync_caption = T("this happens at other shows too", size=SIZE_HEADLINE,
                               color=PALETTE["body"])
        self.place_body(crowdsync_caption, hdr)
        self.play(FadeIn(crowdsync_caption, shift=UP * 0.2), run_time=0.5)
        self.next_slide()
        self.clear_instantly(hdr, crowdsync_caption)

        self.next_slide(
            loop=True,
            src=Path("assets/crowd-pixel/crowdsync_examples_combined.mp4"),
        )
        self.next_slide()
        hdr = self.section_header(title, color=TWICE_PINK, badge=icon_stick())

        dots, info = crowd_grid()
        caption = T("a stadium is just a very low-resolution screen", size=18,
                     color=PALETTE["body"])
        caption.next_to(dots, DOWN, buff=0.4)
        self.place_body(VGroup(dots, caption), hdr)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],
                               lag_ratio=0.0025, run_time=1.6))

        def alpha_for(x):
            return max(0.0, min(1.0, (x + 3.0) / 6.0))

        lit_idx = [i for i in range(len(dots)) if in_twice_logo(*info[i])]
        self.play(LaggedStart(*[
            dots[i].animate.set_fill(grad(alpha_for(info[i][0])), 0.95)
            for i in lit_idx
        ], lag_ratio=0.003, run_time=1.6))
        self.play(FadeIn(caption), run_time=0.5)
        self.next_slide()
        self.play(FadeOut(dots), FadeOut(caption), run_time=0.6)

        photo_caption = T("real footage — Nissan Stadium, seat-mapped",
                           size=SIZE_HEADLINE, color=PALETTE["body"])
        self.place_body(photo_caption, hdr)
        self.play(FadeIn(photo_caption, shift=UP * 0.2), run_time=0.5)
        self.next_slide()
        self.clear_instantly(hdr, photo_caption)

        self.next_slide(
            loop=True,
            src=Path("assets/crowd-pixel/06_cutaways_framed.mp4"),
        )
        self.next_slide()
        hdr = self.section_header(title, color=TWICE_PINK, badge=icon_stick())

        gatt_tag = T("V3 · GATT", size=SIZE_CAPTION, color=TWICE_PINK, weight=BOLD)
        gatt_label = T("services and characteristics.\n"
                        "read · write · subscribe", size=SIZE_BODY, color=PALETTE["body"])
        gatt_group = VGroup(gatt_tag, gatt_label).arrange(DOWN, buff=0.3)
        self.place_body(gatt_group, hdr)
        self.play(FadeIn(gatt_group, shift=UP * 0.2), run_time=0.5)
        self.next_slide()
        self.play(FadeOut(gatt_group), run_time=0.4)

        phone = box("phone", "app", color=PALETTE["body"], w=1.8, h=0.8)
        phone.to_edge(LEFT, buff=1.6)
        stick_icon = icon_stick(size=0.8)
        stick_icon.to_edge(RIGHT, buff=1.8)
        stick_icon.align_to(phone, UP)
        wire = DashedLine(phone.get_right(), stick_icon.get_left(),
                          color=PALETTE["body"], stroke_width=2)
        frame = hex_row(["FF", "C5", "0F", "3A", "00", "1E", "FF"], color=TWICE_PINK)
        frame.next_to(wire, DOWN, buff=0.9)
        frame_label = T("V3 frame", size=SIZE_CAPTION, color=TWICE_PINK)
        frame_label.next_to(frame, UP, buff=0.25)
        op = brace_lab(frame[0], "op code", color=TWICE_PEACH)
        colour = brace_lab(frame[1:5], "colour", color=TWICE_PINK)
        term_b = brace_lab(frame[5:], "terminator", color=TWICE_PEACH)
        credit = T("credit: maximus64/candybong", size=14, color=PALETTE["body"])
        credit.next_to(VGroup(op, colour, term_b), DOWN, buff=0.5)
        self.place_body(
            VGroup(phone, stick_icon, wire, frame, frame_label, op, colour, term_b,
                   credit),
            hdr,
        )
        path = Line(phone.get_right(), stick_icon.get_left())
        packet = Dot(radius=0.1, color=TWICE_PINK, fill_opacity=1)
        packet.move_to(phone.get_right())

        self.play(FadeIn(phone), FadeIn(stick_icon), Create(wire), run_time=0.5)
        self.play(MoveAlongPath(packet, path, run_time=1.0, rate_func=linear))
        self.play(Flash(stick_icon, color=TWICE_GLOW, flash_radius=0.6))
        self.play(LaggedStart(*[GrowFromCenter(c) for c in frame], lag_ratio=0.08,
                               run_time=1.0), FadeIn(frame_label))
        self.play(FadeIn(op), FadeIn(colour), FadeIn(term_b), FadeIn(credit),
                   run_time=0.6)
        self.next_slide()
        self.play(FadeOut(phone), FadeOut(stick_icon), FadeOut(wire), FadeOut(packet),
                  FadeOut(op), FadeOut(colour), FadeOut(term_b), FadeOut(credit),
                  FadeOut(frame), FadeOut(frame_label),
                  run_time=0.6)

        route_a2 = box("Radio Frequency", "capture sub-GHz traffic blind",
                       color=PALETTE["body"], w=3.6, h=1.1, size=20)
        route_v1 = box("Reverse engineer V1 app", "jar files → command codes",
                       color=TWICE_PEACH, w=4.2, h=1.1, size=18)
        routes_v1 = VGroup(route_a2, route_v1).arrange(RIGHT, buff=1.0)
        self.place_body(routes_v1, hdr)
        self.play(FadeIn(route_a2, shift=UP * 0.2), FadeIn(route_v1, shift=UP * 0.2),
                   run_time=0.6)
        self.play(route_a2.animate.set_opacity(0.3),
                   Circumscribe(route_v1, color=TWICE_PEACH, run_time=1.0))
        self.next_slide()
        self.play(FadeOut(routes_v1), run_time=0.5)

        frame_v1 = hex_row(["A5", "01", "FF", "80", "10", "5A"], color=TWICE_PEACH)
        frame_v1.move_to(frame)
        label_v1 = T("V1 frame", size=SIZE_CAPTION, color=TWICE_PEACH)
        label_v1.move_to(frame_label)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in frame_v1], lag_ratio=0.08,
                               run_time=1.0), FadeIn(label_v1))
        self.next_slide()
        self.play(FadeOut(frame_v1), FadeOut(label_v1), run_time=0.5)

        rig_note = VGroup(*[
            T(s, size=SIZE_BODY, color=PALETTE["body"]) for s in [
                "V1 + V3 + accelerometer on a breadboard.",
                "Using both Bluetooth protocols.",
            ]
        ]).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        self.place_body(rig_note, hdr)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in rig_note],
                               lag_ratio=0.3, run_time=1.0))
        self.next_slide()
        self.play(FadeOut(rig_note), run_time=0.5)

        rig_caption = T("driving both sticks, live", size=SIZE_HEADLINE,
                         color=TWICE_PINK)
        self.place_body(rig_caption, hdr)
        self.play(FadeIn(rig_caption, shift=UP * 0.2), run_time=0.5)
        self.next_slide()
        self.clear_instantly(hdr, rig_caption)
        self.next_slide(
            src=Path("assets/demos/lightstick_framed.mp4"),
        )
        self.next_slide()
        hdr = self.section_header(title, color=TWICE_PINK, badge=icon_stick())
        self.next_slide()
        self.play(FadeOut(hdr), run_time=0.6)


    def _close(self):
        hdr = self.section_header("Implorations")

        lessons = VGroup(*[
            T("· " + s, size=SIZE_CAPTION, color=PALETTE["body"]) for s in [
                "AI can do so much with MicroPython",
                "Using microcontrollers is something you can literally do "
                "in a work night, not a weekend",
            ]
        ]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        self.place_body(lessons, hdr)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in lessons],
                               lag_ratio=0.2, run_time=1.4))
        self.next_slide()
        self.play(FadeOut(hdr), FadeOut(lessons), run_time=0.6)

        thanks = T("Thank You!", size=64, color=PALETTE["title"], weight=BOLD)
        thanks.shift(UP * 0.4)
        thanks_line = Line(thanks.get_corner(DOWN + LEFT) + DOWN * 0.25,
                            thanks.get_corner(DOWN + RIGHT) + DOWN * 0.25,
                            color=PALETTE["accent"], stroke_width=3)

        gh_logo = SVGMobject("assets/github.svg")
        gh_logo.set_fill(PALETTE["body"], opacity=1).set_stroke(width=0)
        gh_logo.set(height=0.2)
        py_logo = SVGMobject("assets/python.svg")
        py_logo.set_fill(PALETTE["body"], opacity=1).set_stroke(width=0)
        py_logo.set(height=0.22)
        site_row = VGroup(
            T("cyra.locs.in", size=18, color=PALETTE["accent"]),
            T("·", size=18, color=PALETTE["body"]),
            gh_logo,
            T("@cyra", size=18, color=PALETTE["body"]),
        ).arrange(RIGHT, buff=0.14)
        py_row = VGroup(py_logo, T("Python WA", size=18, color=PALETTE["body"])).arrange(
            RIGHT, buff=0.14
        )
        closing_byline = VGroup(site_row, py_row).arrange(DOWN, buff=0.2)
        closing_byline.next_to(thanks_line, DOWN, buff=0.7)
        closer = factoid("this deck is Python too — built with Manim")
        self.play(Write(thanks), run_time=0.9)
        self.play(FadeIn(thanks_line), FadeIn(closing_byline), run_time=0.5)
        self.play(FadeIn(closer, shift=UP * 0.15), run_time=0.4)
        self.next_slide()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    palette = mo.ui.dropdown(options=list(PALETTES), value="pine", label="palette")
    palette
    return (palette,)


@app.cell
def _(mo, palette):
    import subprocess

    Deck

    subprocess.run(
        ["uv", "run", "manim-slides", "render", "-ql", "deck.py", "Deck"],
        check=True,
        env={**os.environ, "DECK_PALETTE": palette.value},
    )
    subprocess.run(
        ["uv", "run", "manim-slides", "convert", "Deck", "preview.html",
         "--one-file", "-c", "controls=true"],
        check=True,
    )
    mo.iframe(Path("preview.html").read_text(), height="480px")
    return


if __name__ == "__main__":
    app.run()
