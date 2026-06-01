"""
彩虹六号 · 随机干员选择器 — Python GUI 版
CSGO 开箱风滚动动画 + 玻璃拟态 UI
"""
import tkinter as tk
from tkinter import font as tkfont
import random
import math
import threading
import time

# ==================== 干员数据 ====================
ATTACKERS = [
    "Sledge","Thatcher","Ash","Thermite","Twitch","Montagne","Glaz","Fuze","Blitz","IQ","Buck",
    "Blackbeard","Capitao","Hibana","Jackal","Ying","Zofia","Dokkaebi","Lion","Finka","Maverick",
    "Nomad","Gridlock","Nøkk","Amaru","Kali","Iana","Ace","Zero","Flores","Osa","Sens","Brava","Ram",
    "Deimos","Rauora","Solid Snake"
]
DEFENDERS = [
    "Smoke","Mute","Castle","Pulse","Doc","Rook","Kapkan","Tachanka","Jager","Bandit","Frost",
    "Valkyrie","Caveira","Echo","Mira","Lesion","Ela","Vigil","Maestro","Alibi","Clash",
    "Kaid","Mozzie","Warden","Goyo","Wamai","Oryx","Melusi","Aruni","Thunderbird","Azami","Solis",
    "Fenrir","Thron","Tubarão","Skopós","Denari"
]

# ==================== 主窗口 ====================
class R6OperatorPicker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("R6 随机干员选择器")
        self.window.configure(bg="#0a0a12")
        self.window.geometry("520x680")
        self.window.minsize(420, 580)
        self.window.resizable(True, True)

        # 状态
        self.current_side = None  # 'attacker' | 'defender'
        self.is_spinning = False
        self.history = []
        self.spin_animation_running = False

        # 字体
        self.font_title = tkfont.Font(family="Microsoft YaHei", size=22, weight="bold")
        self.font_subtitle = tkfont.Font(family="Microsoft YaHei", size=10)
        self.font_side = tkfont.Font(family="Microsoft YaHei", size=13, weight="bold")
        self.font_small = tkfont.Font(family="Microsoft YaHei", size=9)
        self.font_badge = tkfont.Font(family="Microsoft YaHei", size=8, weight="bold")

        # 构建UI
        self.build_ui()

    # ==================== UI构建 ====================
    def build_ui(self):
        bg = "#0a0a12"

        # 主容器
        self.main_frame = tk.Frame(self.window, bg=bg)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== 标题 =====
        title_frame = tk.Frame(self.main_frame, bg=bg)
        title_frame.pack(fill="x", pady=(5, 20))

        # 徽章
        badge_frame = tk.Frame(title_frame, bg="#1a1a24", bd=0, highlightbackground="#ff6a00", highlightthickness=1)
        badge_frame.pack()
        tk.Label(badge_frame, text="  SIEGE v1.0  ", font=self.font_badge,
                 fg="#ff6a00", bg="#1a1a24").pack(padx=2, pady=1)

        # 标题
        tk.Label(title_frame, text="RANDOM OPERATOR",
                 font=self.font_title, fg="#ff8c00", bg=bg).pack()

        # 副标题
        tk.Label(title_frame, text="随机干员选择器",
                 font=self.font_subtitle, fg="#555566", bg=bg).pack()

        # 分隔线
        sep_frame = tk.Frame(title_frame, height=2, bg="#ff6a00")
        sep_frame.pack(fill="x", pady=6)

        # ===== 阵营选择 =====
        side_frame = tk.Frame(self.main_frame, bg=bg)
        side_frame.pack(fill="x", pady=(0, 15))

        self.btn_att = self.make_side_button(side_frame, "attacker", "进攻方", "#004488", "#66ccff")
        self.btn_att.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_def = self.make_side_button(side_frame, "defender", "防守方", "#661100", "#ff5a33")
        self.btn_def.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # ===== Slot Machine =====
        self.slot_frame = tk.Frame(self.main_frame, bg="#0d0d18",
                                   highlightbackground="#1a1a2e", highlightthickness=1, bd=0)
        self.slot_frame.pack(fill="x", pady=(0, 15))

        # 上方标签
        self.slot_label = tk.Label(self.slot_frame, text="— SELECT SIDE —",
                                   font=self.font_small, fg="#555566", bg="#0d0d18")
        self.slot_label.pack(fill="x", pady=(8, 0))

        # Canvas 滚动区域
        self.slot_canvas = tk.Canvas(self.slot_frame, height=100,
                                     bg="#08080f", highlightthickness=0)
        self.slot_canvas.pack(fill="x", padx=4)

        # 占位文字
        self.slot_canvas.create_text(260, 50, text="??",
                                     fill="#1a1a2e",
                                     font=("Microsoft YaHei", 28, "bold"))

        # 底部状态栏
        slot_footer = tk.Frame(self.slot_frame, bg="#0d0d18")
        slot_footer.pack(fill="x", padx=12, pady=(2, 6))

        self.slot_count = tk.Label(slot_footer, text="",
                                   font=self.font_small, fg="#555566",
                                   bg="#0d0d18")
        self.slot_count.pack(side="left")

        self.slot_result = tk.Label(slot_footer, text="等待开始",
                                    font=self.font_small, fg="#555566",
                                    bg="#0d0d18")
        self.slot_result.pack(side="right")

        # ===== 抽选按钮 =====
        self.pick_btn = tk.Button(self.main_frame,
                                  text="SELECT SIDE FIRST",
                                  font=self.font_side,
                                  bg="#1a1a24",
                                  fg="#555566",
                                  relief="flat",
                                  bd=0,
                                  padx=10, pady=14,
                                  cursor="hand2",
                                  state="disabled",
                                  command=self.start_spin)
        self.pick_btn.pack(fill="x", pady=(0, 12))

        # ===== 历史记录 =====
        history_frame = tk.Frame(self.main_frame, bg=bg)
        history_frame.pack(fill="x")

        hist_top = tk.Frame(history_frame, bg=bg)
        hist_top.pack(fill="x")

        tk.Label(hist_top, text="记录", font=self.font_small,
                 fg="#9999aa", bg=bg).pack(side="left")

        self.hist_count = tk.Label(hist_top, text="0",
                                   font=self.font_small,
                                   fg="#555566", bg="#0d0d18",
                                   padx=6, pady=1)
        self.hist_count.pack(side="left", padx=6)

        self.clear_btn = tk.Label(hist_top, text="X",
                                  font=self.font_small,
                                  fg="#555566", bg=bg,
                                  cursor="hand2")
        self.clear_btn.pack(side="right")
        self.clear_btn.bind("<Button-1>", lambda e: self.clear_history())
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(fg="#ff5555"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(fg="#555566"))

        # 历史列表容器
        self.hist_container = tk.Frame(history_frame, bg=bg)
        self.hist_container.pack(fill="x", pady=(5, 0))

        # ===== 底部链接 =====
        tk.Label(self.main_frame, text="查看全部干员",
                 font=self.font_small, fg="#555566", bg=bg,
                 cursor="hand2").pack(pady=(8, 0))
        # 这里通过bind事件实现

    def make_side_button(self, parent, side, text, active_bg, active_fg):
        btn = tk.Button(parent, text=text,
                        font=self.font_side,
                        bg="#0d0d18",
                        fg="#555566",
                        relief="flat", bd=0,
                        cursor="hand2",
                        padx=10, pady=12,
                        activebackground="#1a1a24",
                        activeforeground="#9999aa")
        btn.config(command=lambda s=side: self.select_side(s))
        btn.bind("<Enter>", lambda e, b=btn: self.on_btn_hover(b, True, side))
        btn.bind("<Leave>", lambda e, b=btn: self.on_btn_hover(b, False, side))
        return btn

    def on_btn_hover(self, btn, enter, side):
        if enter and side != self.current_side:
            btn.config(bg="#1a1a24")
        elif not enter and side != self.current_side:
            btn.config(bg="#0d0d18")

    # ==================== 阵营选择 ====================
    def select_side(self, side):
        if self.is_spinning:
            return
        self.current_side = side

        # 更新按钮样式
        atk_bg = "#002266" if side == "attacker" else "#0d0d18"
        atk_fg = "#66ccff" if side == "attacker" else "#555566"
        def_bg = "#661100" if side == "defender" else "#0d0d18"
        def_fg = "#ff5a33" if side == "defender" else "#555566"

        self.btn_att.config(bg=atk_bg, fg=atk_fg)
        self.btn_def.config(bg=def_bg, fg=def_fg)

        pool = ATTACKERS if side == "attacker" else DEFENDERS
        side_name = "ATTACKER" if side == "attacker" else "DEFENDER"

        slot_color = "#0066aa" if side == "attacker" else "#aa3300"
        self.slot_label.config(text=f"{side_name}", fg=slot_color)
        self.slot_count.config(text=f"共 {len(pool)} 名干员", fg=slot_color)

        # 更新Canvas就绪状态
        self.slot_canvas.delete("all")
        ready_color = "#006699" if side == "attacker" else "#993300"
        self.slot_canvas.create_text(260, 50, text="就绪",
                                     fill=ready_color,
                                     font=("Microsoft YaHei", 18, "bold"))

        self.slot_result.config(text="开始抽选吧")

        # 启用按钮
        btn_bg = "#004488" if side == "attacker" else "#882200"
        btn_fg = "#ffffff"
        self.pick_btn.config(state="normal", text="开始滚动抽选",
                             bg=btn_bg, fg=btn_fg,
                             activebackground="#0055aa" if side == "attacker" else "#aa3300")

    # ==================== 滚动抽选 ====================
    def start_spin(self):
        if self.is_spinning or not self.current_side:
            return
        self.is_spinning = True

        pool = ATTACKERS if self.current_side == "attacker" else DEFENDERS
        # 让最终结果随机，且在半秒前确定
        self.final_result = random.choice(pool)

        self.pick_btn.config(state="disabled", text="滚动中...",
                             bg="#1a1a24", fg="#555566")

        # 启动动画线程
        threading.Thread(target=self.spin_animation_thread,
                         daemon=True).start()

    def spin_animation_thread(self):
        pool = ATTACKERS if self.current_side == "attacker" else DEFENDERS
        is_atk = self.current_side == "attacker"

        # 颜色
        colors = ["#002244", "#004488", "#0066aa",
                   "#66ccff"] if is_atk else [
                   "#220000", "#550000", "#882200", "#ff5a33"]
        bright_color = "#66ccff" if is_atk else "#ff6a33"

        start_time = time.time()
        duration = 2.0 + random.random() * 0.8
        high_speed_count = 0

        while True:
            elapsed = time.time() - start_time
            progress = min(elapsed / duration, 1.0)

            # easeOutQuart
            eased = 1 - (1 - progress) ** 4

            # 当前显示的干员（在中间）
            idx = int(eased * len(pool) * 10) % len(pool)
            current_name = pool[idx]

            slowed = progress > 0.8

            # 最后的阶段逐渐减速
            display_count = 1
            if slowed:
                display_count = 1
                # 接近最终结果
                if progress > 0.92:
                    current_name = self.final_result

            # 主线程更新
            self.window.after(0, self.update_canvas, current_name, bright_color, progress)

            if progress >= 1.0:
                break

            # 等待时间 - 减速
            if progress > 0.85:
                time.sleep(0.05 + (progress - 0.85) * 0.3)
            elif progress > 0.7:
                time.sleep(0.03)
            else:
                time.sleep(0.016)

        # 完成
        self.window.after(0, self.finish_spin)

    def update_canvas(self, name, color, progress):
        self.slot_canvas.delete("all")

        pool = ATTACKERS if self.current_side == "attacker" else DEFENDERS
        is_atk = self.current_side == "attacker"

        cw = self.slot_canvas.winfo_width() or 480
        item_h = 36

        # 当前显示在中间，上下各显示2个
        visible_ops = []
        pool_len = len(pool)

        # 找当前name的索引
        try:
            current_idx = pool.index(name)
        except ValueError:
            current_idx = 0

        for offset in range(-2, 3):
            idx = (current_idx + offset) % pool_len
            op_name = pool[idx]
            y_pos = 50 + offset * item_h

            # 透明度/亮度
            dist = abs(offset)
            alpha = max(0.15, 1.0 - dist * 0.4)

            if is_atk:
                r, g, b = int(50 + 180 * alpha), int(100 + 155 * alpha), int(180 + 75 * alpha)
            else:
                r, g, b = int(200 + 55 * alpha), int(60 * alpha), int(30 * alpha)

            hex_c = f"#{r:02x}{g:02x}{b:02x}"
            font_size = 22 - dist * 3

            # 中间高亮
            if offset == 0:
                hex_c = "#ffffff"
                font_size = 26

            self.slot_canvas.create_text(
                cw // 2, y_pos,
                text=op_name,
                fill=hex_c,
                font=("Microsoft YaHei", font_size, "bold"),
                anchor="center"
            )

        # 更新结果标签
        if progress > 0.9:
            self.slot_result.config(text=name)
        else:
            self.slot_result.config(text="...")

    def finish_spin(self):
        self.is_spinning = False
        cw = self.slot_canvas.winfo_width() or 480
        self.slot_canvas.delete("all")

        is_atk = self.current_side == "attacker"
        color = "#66ccff" if is_atk else "#ff6a33"

        # 最终大结果
        self.slot_canvas.create_text(
            cw // 2, 50,
            text=self.final_result,
            fill=color,
            font=("Microsoft YaHei", 32, "bold"),
            anchor="center"
        )

        self.slot_result.config(text=self.final_result)

        # 恢复按钮
        btn_bg = "#004488" if is_atk else "#882200"
        self.pick_btn.config(state="normal", text="再来一次",
                             bg=btn_bg, fg="#ffffff",
                             activebackground="#0055aa" if is_atk else "#aa3300")

        # 添加历史
        self.add_history(self.final_result)

    # ==================== 历史记录 ====================
    def add_history(self, op):
        self.history.insert(0, {"operator": op, "side": self.current_side})
        if len(self.history) > 30:
            self.history.pop()
        self.render_history()

    def clear_history(self):
        self.history = []
        self.render_history()

    def render_history(self):
        for w in self.hist_container.winfo_children():
            w.destroy()

        bg = "#0a0a12"
        self.hist_count.config(text=str(len(self.history)))

        if len(self.history) == 0:
            tk.Label(self.hist_container, text="暂无记录",
                     font=self.font_small, fg="#222233",
                     bg=bg).pack()
            return

        for item in self.history[:20]:
            side = item["side"]
            color_bg = "#001122" if side == "attacker" else "#110500"
            color_fg = "#4488bb" if side == "attacker" else "#bb5533"

            lbl = tk.Label(self.hist_container,
                           text=item['operator'],
                           font=self.font_small,
                           bg=color_bg, fg=color_fg,
                           padx=6, pady=2, bd=0)
            lbl.pack(side="left", padx=2, pady=2)

    # ==================== 启动 ====================
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = R6OperatorPicker()
    app.run()
