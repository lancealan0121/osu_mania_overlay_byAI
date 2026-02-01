import sys
import json
import time
import keyboard
import os
import random
import math
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QColorDialog, QTabWidget, QFormLayout,
                               QSpinBox, QLineEdit, QPushButton, QCheckBox, QSlider,
                               QComboBox, QDoubleSpinBox, QGroupBox, QScrollArea)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QRectF, QPointF, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import (QPainter, QColor, QBrush, QPen, QFont, QLinearGradient,
                           QRadialGradient, QPainterPath)


#  pyinstaller --onefile --windowed --clean --icon=icon.ico --add-data "languages;languages" main.py
# made by yulun, yulun fucked ai generated
class TranslationManager:
    def __init__(self):
        self.translations = {}
        self.current_language = "zh_TW"
        self.load_translations()

    def load_translations(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        lang_dir = os.path.join(base_path, "languages")

        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
            self.load_fallback_translations()
            return

        loaded_count = 0
        for filename in os.listdir(lang_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]
                try:
                    filepath = os.path.join(lang_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                        loaded_count += 1
                except:
                    pass

        if loaded_count == 0:
            self.load_fallback_translations()

    def load_fallback_translations(self):
        self.translations = {
            "zh_TW": {
                "window_title": "OL Mode v1 - 增強設定",
                "save_button": "儲存設定",
                "language": "語言:",
                "language_note": "請將語言檔案放入 languages 資料夾",
            },
            "en_US": {
                "window_title": "OL Mode v1 - Settings",
                "save_button": "Save Settings",
                "language": "Language:",
                "language_note": "Please place language files in languages folder",
            }
        }

    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False

    def get(self, key, lang=None):
        if lang is None:
            lang = self.current_language
        if lang not in self.translations:
            lang = "zh_TW"
        return self.translations.get(lang, {}).get(key, key)

    def get_available_languages(self):
        lang_names = {
            "zh_TW": "繁體中文", "en_US": "English", "ja_JP": "日本語",
            "ko_KR": "한국어", "zh_CN": "简体中文", "es_ES": "Español",
            "fr_FR": "Français", "de_DE": "Deutsch", "ru_RU": "Русский",
            "pt_BR": "Português",
        }
        return [(code, lang_names.get(code, code)) for code in sorted(self.translations.keys())]


translation_manager = TranslationManager()


def t(key):
    return translation_manager.get(key)


CONFIG_FILE = "osu_OL_v1_config.json"
DEFAULT_CONFIG = {
    "key_count": 4,
    "keys": ["d", "f", "j", "k"],
    "colors": ["#00E5FF", "#00FF88", "#FF0077", "#FFD600"],
    "width": 70, "height": 50, "spacing": 12, "fps_limit": 144,
    "max_kps": 32, "kps_font_size": 20, "kps_pos_x": 0, "kps_pos_y": 10,
    "spring_stiffness": 25, "press_scale": 85,
    "enable_vis": True, "vis_height": 400, "vis_speed": 8, "vis_opacity": 180,
    "enable_part": True, "part_count": 12, "part_gravity": 40, "part_force": 60, "part_decay": 30,
    "enable_glow": True, "glow_spread": 25, "glow_intensity": 150, "glow_decay": 8,
    "enable_ripple": True, "ripple_speed": 5,
    "window_x": 100, "window_y": 100, "settings_x": 600, "settings_y": 100,
    "animation_style": "default", "key_shape": "rounded", "background_opacity": 0,
    "enable_rainbow": False, "rainbow_speed": 5,
    "enable_trail": True, "trail_length": 5,
    "enable_shake": False, "shake_intensity": 5,
    "enable_combo": True, "combo_reset_time": 2.0,
    "press_sound": False, "border_width": 2, "border_glow": True, "rotation_on_press": 0,
    "enable_wave_distortion": False, "wave_amplitude": 10, "wave_frequency": 2,
    "glow_color_mode": "key", "glow_custom_color": "#FF0099",
    "particle_shape": "circle", "particle_size_min": 2, "particle_size_max": 6,
    "enable_stats": True, "total_presses": 0, "session_start": 0,
    "show_key_count": True, "key_count_font_size": 12, "key_count_color": "#FFFFFF",
    "show_kps": True, "kps_color_change": True, "kps_custom_color": "#FFFFFF",
    "vis_gradient": True, "show_max_kps": True,
    "max_kps_pos_x": 0, "max_kps_pos_y": 50, "max_kps_color": "#FFD700",
    "language": "zh_TW", "auto_switch_max": True, "switch_delay": 5.0,
    "toggle_settings_key": "f1",
    "use_custom_positions": False,  # 新增：是否使用自定義位置
    "key_custom_positions": [],  # 新增：每個按鍵的自定義位置 [{"x": 0, "y": 0}, ...]
}


class ConfigManager:
    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self.load()
        self.data["max_kps_record"] = 0
        translation_manager.set_language(self.data.get("language", "zh_TW"))

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except:
                pass

    def save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)


cfg = ConfigManager()


class Particle:
    def __init__(self, x, y, color):
        self.pos = QPointF(x, y)
        f = cfg.data["part_force"] / 10.0
        self.vel = QPointF(random.uniform(-f, f), random.uniform(-f * 1.5, -f * 0.5))
        self.life = 1.0
        self.color = QColor(color)
        self.size = random.uniform(cfg.data["particle_size_min"], cfg.data["particle_size_max"])
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-10, 10)

    def update(self):
        self.pos += self.vel
        self.vel.setY(self.vel.y() + (cfg.data["part_gravity"] / 100.0))
        self.life -= (cfg.data["part_decay"] / 1000.0)
        self.rotation += self.rot_speed


class TrailPoint:
    def __init__(self, y, h):
        self.y = y
        self.h = h
        self.opacity = 1.0


class KeyState:
    def __init__(self, label, color_hex):
        self.label = label
        self.color = QColor(color_hex)
        self.is_pressed = False
        self.press_count = 0
        self.curr_scale = 1.0
        self.glow_pulse = 0.0
        self.active_notes = []
        self.particles = []
        self.trail_points = []
        self.shake_offset = QPointF(0, 0)
        self.rotation = 0
        self.wave_offset = 0
        self.last_press_time = 0
        self.combo = 0
        self.was_pressed = False

    def press(self, x_c, y_c):
        if not self.was_pressed:
            self.was_pressed = True
            self.is_pressed = True
            self.press_count += 1
            self.glow_pulse = 1.0

            current_time = time.time()
            if current_time - self.last_press_time <= cfg.data["combo_reset_time"]:
                self.combo += 1
            else:
                self.combo = 1
            self.last_press_time = current_time
            cfg.data["total_presses"] += 1

            if cfg.data["enable_vis"]:
                self.active_notes.append({"y": 0, "h": 0, "done": False})
            if cfg.data["enable_part"]:
                for _ in range(cfg.data["part_count"]):
                    self.particles.append(Particle(x_c, y_c, self.color))
        else:
            self.is_pressed = True

    def release(self):
        if self.was_pressed:
            self.was_pressed = False
            self.is_pressed = False
            if self.active_notes:
                self.active_notes[-1]["done"] = True

    def update(self, time_delta):
        if time.time() - self.last_press_time > cfg.data["combo_reset_time"]:
            self.combo = 0

        anim = cfg.data["animation_style"]
        target = (cfg.data["press_scale"] / 100.0) if self.is_pressed else 1.0

        if anim == "wave":
            self.wave_offset += 0.1
            target += math.sin(self.wave_offset) * 0.05
        elif anim == "pulse":
            if self.is_pressed:
                target = 0.85 + abs(math.sin(time.time() * 10)) * 0.15
        elif anim == "bounce":
            if self.is_pressed and self.curr_scale > target:
                target *= 0.7

        self.curr_scale += (target - self.curr_scale) * (cfg.data["spring_stiffness"] / 100.0)

        if cfg.data["rotation_on_press"] > 0:
            target_rot = cfg.data["rotation_on_press"] if self.is_pressed else 0
            self.rotation += (target_rot - self.rotation) * 0.2

        if cfg.data["enable_shake"] and self.is_pressed:
            intensity = cfg.data["shake_intensity"] / 10.0
            self.shake_offset.setX(random.uniform(-intensity, intensity))
            self.shake_offset.setY(random.uniform(-intensity, intensity))
        else:
            self.shake_offset *= 0.8

        self.glow_pulse *= (1.0 - (cfg.data["glow_decay"] / 100.0))

        speed = cfg.data["vis_speed"]
        for n in self.active_notes:
            n["y"] -= speed
            if not n["done"]:
                n["h"] += speed
        self.active_notes = [n for n in self.active_notes if (n["y"] + n["h"]) > -cfg.data["vis_height"]]

        if cfg.data["enable_trail"] and self.active_notes:
            for note in self.active_notes:
                if not note["done"] and random.random() < 0.3:
                    self.trail_points.append(TrailPoint(note["y"], note["h"]))

        for t in self.trail_points:
            t.opacity -= 0.02
        self.trail_points = [t for t in self.trail_points if t.opacity > 0]

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        self.resize(320, 300)
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        self.opacity_value = 0.0
        self.scale_value = 0.5
        self.rotation_value = 0.0

        self.opacity_anim = QPropertyAnimation(self, b"opacity_val")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.scale_anim = QPropertyAnimation(self, b"scale_val")
        self.scale_anim.setDuration(800)
        self.scale_anim.setStartValue(0.5)
        self.scale_anim.setEndValue(1.0)
        self.scale_anim.setEasingCurve(QEasingCurve.OutElastic)

        self.rotation_anim = QPropertyAnimation(self, b"rotation_val")
        self.rotation_anim.setDuration(800)
        self.rotation_anim.setStartValue(-180.0)
        self.rotation_anim.setEndValue(0.0)
        self.rotation_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.fade_out_anim = QPropertyAnimation(self, b"opacity_val")
        self.fade_out_anim.setDuration(500)
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.finished.connect(self.close)

        QTimer.singleShot(2000, self.start_fade_out)

    def start_fade_out(self):
        self.fade_out_anim.start()

    def get_opacity_val(self):
        return self.opacity_value

    def set_opacity_val(self, value):
        self.opacity_value = value
        self.update()

    opacity_val = Property(float, get_opacity_val, set_opacity_val)

    def get_scale_val(self):
        return self.scale_value

    def set_scale_val(self, value):
        self.scale_value = value
        self.update()

    scale_val = Property(float, get_scale_val, set_scale_val)

    def get_rotation_val(self):
        return self.rotation_value

    def set_rotation_val(self, value):
        self.rotation_value = value
        self.update()

    rotation_val = Property(float, get_rotation_val, set_rotation_val)

    def showEvent(self, event):
        super().showEvent(event)
        self.opacity_anim.start()
        self.scale_anim.start()
        self.rotation_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self.opacity_value)

        rect = self.rect()
        painter.save()
        painter.translate(rect.center())
        painter.scale(self.scale_value, self.scale_value)
        painter.rotate(self.rotation_value)
        painter.translate(-rect.center())

        gradient = QRadialGradient(rect.center(), 200)
        gradient.setColorAt(0, QColor(60, 60, 60, 230))
        gradient.setColorAt(1, QColor(20, 20, 20, 250))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.drawRoundedRect(rect.adjusted(20, 20, -20, -20), 40, 40)

        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Microsoft JhengHei UI", 32, QFont.Bold))
        title_rect = QRectF(0, 80, rect.width(), 60)
        painter.drawText(title_rect, Qt.AlignCenter, "osu! OL")

        painter.setPen(QColor(180, 180, 180))
        painter.setFont(QFont("Microsoft JhengHei UI", 18))
        version_rect = QRectF(0, 140, rect.width(), 40)
        painter.drawText(version_rect, Qt.AlignCenter, t("version"))

        painter.setPen(QColor(150, 150, 150))
        painter.setFont(QFont("Microsoft JhengHei UI", 12))
        loading_rect = QRectF(0, 200, rect.width(), 30)
        painter.drawText(loading_rect, Qt.AlignCenter, t("loading"))

        painter.restore()


class OLOverlay(QWidget):

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.keys_state, self.kps_buffer = [], []
        self.rainbow_hue = 0
        self.last_time = time.time()
        self.move(cfg.data["window_x"], cfg.data["window_y"])
        self.last_key_press_time = time.time()

        # 新增：拖動相關變數
        self.dragging_key_index = -1  # -1 表示拖動整個窗口
        self.drag_start_pos = QPointF(0, 0)

        self.setup_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(int(1000 / cfg.data["fps_limit"]))

        if cfg.data["session_start"] == 0:
            cfg.data["session_start"] = time.time()

        self.hide()

    def setup_ui(self):
        # 修復1: 保留現有的 press_count
        old_states = {}
        if self.keys_state:
            for i, state in enumerate(self.keys_state):
                old_states[i] = {
                    'press_count': state.press_count,
                    'combo': state.combo
                }

        self.keys_state = []
        for i in range(cfg.data["key_count"]):
            l = cfg.data["keys"][i] if i < len(cfg.data["keys"]) else "?"
            c = cfg.data["colors"][i] if i < len(cfg.data["colors"]) else "#FFFFFF"
            new_state = KeyState(l, c)

            # 恢復舊的計數
            if i in old_states:
                new_state.press_count = old_states[i]['press_count']
                new_state.combo = old_states[i]['combo']

            self.keys_state.append(new_state)

        # 修復3: 確保自定義位置數組長度正確
        if "key_custom_positions" not in cfg.data:
            cfg.data["key_custom_positions"] = []

        # 調整自定義位置數組長度
        while len(cfg.data["key_custom_positions"]) < cfg.data["key_count"]:
            cfg.data["key_custom_positions"].append({"x": 0, "y": 0})

        # 移除多餘的自定義位置
        if len(cfg.data["key_custom_positions"]) > cfg.data["key_count"]:
            cfg.data["key_custom_positions"] = cfg.data["key_custom_positions"][:cfg.data["key_count"]]

        w = (cfg.data["width"] + cfg.data["spacing"]) * cfg.data["key_count"] + 300
        h = cfg.data["vis_height"] + 300
        self.resize(w, h)

    def get_key_position(self, index):
        """獲取按鍵的位置（考慮自定義位置）"""
        kw, spacing = cfg.data["width"], cfg.data["spacing"]
        base_y = cfg.data["vis_height"] + 80

        if cfg.data.get("use_custom_positions", False) and index < len(cfg.data["key_custom_positions"]):
            custom_pos = cfg.data["key_custom_positions"][index]
            return 100 + index * (kw + spacing) + custom_pos["x"], base_y + custom_pos["y"]
        else:
            return 100 + index * (kw + spacing), base_y

    def handle_input(self, name, pressed):
        for i, char in enumerate(cfg.data["keys"]):
            if char.lower() == name.lower():
                x_c, y_c = self.get_key_position(i)
                kw = cfg.data["width"]
                x_c += kw / 2

                if pressed:
                    if not self.keys_state[i].was_pressed:
                        self.kps_buffer.append(time.time())
                        self.last_key_press_time = time.time()
                    self.keys_state[i].press(x_c, y_c)
                else:
                    self.keys_state[i].release()

    def tick(self):
        current_time = time.time()
        time_delta = current_time - self.last_time
        self.last_time = current_time

        now = current_time
        self.kps_buffer = [t for t in self.kps_buffer if now - t <= 1.0]

        current_kps = len(self.kps_buffer)
        if current_kps > cfg.data["max_kps_record"]:
            cfg.data["max_kps_record"] = current_kps

        if cfg.data["enable_rainbow"]:
            self.rainbow_hue = (self.rainbow_hue + cfg.data["rainbow_speed"] / 10.0) % 360

        for k in self.keys_state: k.update(time_delta)
        self.update()

    def get_kps_style(self):
        kps = len(self.kps_buffer)

        if not cfg.data["kps_color_change"]:
            return kps, QColor(cfg.data["kps_custom_color"])

        ratio = min(kps / cfg.data["max_kps"], 1.0)
        if ratio < 0.33:
            col = QColor(255, 255, int(255 * (1 - ratio / 0.33)))
        elif ratio < 0.66:
            sub = (ratio - 0.33) / 0.33
            col = QColor(255, 255 - int(90 * sub), 0)
        else:
            sub = (ratio - 0.66) / 0.34
            col = QColor(255, 165 - int(165 * sub), 0)
        return kps, col

    def draw_key_shape(self, painter, rect, shape):
        if shape == "circle":
            painter.drawEllipse(rect)
        elif shape == "square":
            painter.drawRect(rect)
        elif shape == "hexagon":
            path = QPainterPath()
            w, h = rect.width(), rect.height()
            cx, cy = rect.center().x(), rect.center().y()
            points = []
            for i in range(6):
                angle = math.pi / 3 * i
                x = cx + w / 2 * math.cos(angle)
                y = cy + h / 2 * math.sin(angle)
                points.append(QPointF(x, y))
            path.moveTo(points[0])
            for p in points[1:]:
                path.lineTo(p)
            path.closeSubpath()
            painter.drawPath(path)
        else:
            painter.drawRoundedRect(rect, 6, 6)

    def draw_particle(self, painter, particle):
        shape = cfg.data["particle_shape"]
        size = particle.size * particle.life

        if shape == "square":
            rect = QRectF(particle.pos.x() - size / 2, particle.pos.y() - size / 2, size, size)
            painter.save()
            painter.translate(particle.pos)
            painter.rotate(particle.rotation)
            painter.translate(-particle.pos)
            painter.drawRect(rect)
            painter.restore()
        elif shape == "star":
            painter.save()
            painter.translate(particle.pos)
            painter.rotate(particle.rotation)
            path = QPainterPath()
            for i in range(5):
                angle = math.pi * 2 / 5 * i - math.pi / 2
                outer_x = size * math.cos(angle)
                outer_y = size * math.sin(angle)
                if i == 0:
                    path.moveTo(outer_x, outer_y)
                else:
                    path.lineTo(outer_x, outer_y)
                inner_angle = angle + math.pi / 5
                inner_x = size / 2 * math.cos(inner_angle)
                inner_y = size / 2 * math.sin(inner_angle)
                path.lineTo(inner_x, inner_y)
            path.closeSubpath()
            painter.drawPath(path)
            painter.restore()
        else:
            painter.drawEllipse(particle.pos, size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if cfg.data["background_opacity"] > 0:
            bg = QColor(0, 0, 0, cfg.data["background_opacity"])
            painter.fillRect(self.rect(), bg)

        kw, kh = cfg.data["width"], cfg.data["height"]
        vis_h, spacing = cfg.data["vis_height"], cfg.data["spacing"]

        if cfg.data["show_kps"]:
            idle_time = time.time() - self.last_key_press_time

            should_show_max = (cfg.data["auto_switch_max"] and
                               cfg.data["show_max_kps"] and
                               idle_time >= cfg.data["switch_delay"])

            if should_show_max:
                painter.setPen(QColor(cfg.data["max_kps_color"]))
                painter.setFont(QFont("Microsoft JhengHei UI", cfg.data["kps_font_size"], QFont.Bold))
                kps_rect = QRectF(0, cfg.data["kps_pos_y"], self.width() - 50 + cfg.data["kps_pos_x"], 100)
                painter.drawText(kps_rect, Qt.AlignRight, t("max_display").format(cfg.data['max_kps_record']))
            else:
                kps, k_col = self.get_kps_style()
                painter.setPen(k_col)
                painter.setFont(QFont("Microsoft JhengHei UI", cfg.data["kps_font_size"], QFont.Bold))
                kps_rect = QRectF(0, cfg.data["kps_pos_y"], self.width() - 50 + cfg.data["kps_pos_x"], 100)
                painter.drawText(kps_rect, Qt.AlignRight, t("kps_display").format(kps))

        if cfg.data["show_max_kps"] and not cfg.data["auto_switch_max"]:
            painter.setPen(QColor(cfg.data["max_kps_color"]))
            painter.setFont(QFont("Microsoft JhengHei UI", cfg.data["kps_font_size"], QFont.Bold))
            max_kps_rect = QRectF(0, cfg.data["max_kps_pos_y"], self.width() - 50 + cfg.data["max_kps_pos_x"], 100)
            painter.drawText(max_kps_rect, Qt.AlignRight, t("max_display").format(cfg.data['max_kps_record']))

        if cfg.data["enable_stats"]:
            painter.setPen(QColor(150, 150, 150))
            painter.setFont(QFont("Microsoft JhengHei UI", 12))
            session_time = time.time() - cfg.data["session_start"]
            stats_text = t("stats_display").format(
                cfg.data['total_presses'],
                int(session_time // 60),
                int(session_time % 60)
            )
            painter.drawText(QRectF(10, 10, 400, 30), Qt.AlignLeft, stats_text)

        for idx, k in enumerate(self.keys_state):
            start_x, base_y = self.get_key_position(idx)

            if cfg.data["enable_rainbow"]:
                hue = (self.rainbow_hue + idx * 60) % 360
                color = QColor.fromHsv(int(hue), 255, 255)
            else:
                color = k.color

            if cfg.data["enable_vis"]:
                painter.save()
                painter.setClipRect(start_x, 50, kw, vis_h + 30)

                if cfg.data["enable_trail"]:
                    for t_pt in k.trail_points:
                        rect = QRectF(start_x, base_y + t_pt.y, kw, t_pt.h)
                        trail_color = QColor(color)
                        trail_color.setAlpha(int(cfg.data["vis_opacity"] * t_pt.opacity * 0.5))
                        painter.setBrush(trail_color)
                        painter.setPen(Qt.NoPen)
                        painter.drawRoundedRect(rect, 4, 4)

                for n in k.active_notes:
                    rect = QRectF(start_x, base_y + n["y"], kw, n["h"])

                    if cfg.data["vis_gradient"]:
                        grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
                        c1 = QColor(color)
                        c1.setAlpha(cfg.data["vis_opacity"])
                        grad.setColorAt(0, c1)
                        grad.setColorAt(1, QColor(0, 0, 0, 0))
                        painter.setBrush(grad)
                    else:
                        c1 = QColor(color)
                        c1.setAlpha(cfg.data["vis_opacity"])
                        painter.setBrush(c1)

                    painter.setPen(Qt.NoPen)
                    painter.drawRoundedRect(rect, 4, 4)
                painter.restore()

            if cfg.data["enable_glow"] and k.glow_pulse > 0.01:
                spread = cfg.data["glow_spread"] / 10.0
                radial = QRadialGradient(start_x + kw / 2, base_y + kh / 2, kw * spread)

                glow_mode = cfg.data["glow_color_mode"]
                if glow_mode == "white":
                    glow_color = QColor(255, 255, 255)
                elif glow_mode == "rainbow":
                    glow_color = QColor.fromHsv(int(self.rainbow_hue), 255, 255)
                elif glow_mode == "custom":
                    glow_color = QColor(cfg.data.get("glow_custom_color", "#FF0099"))
                else:
                    glow_color = color

                alpha = int(cfg.data["glow_intensity"] * k.glow_pulse)
                glow_color.setAlpha(alpha)
                radial.setColorAt(0, glow_color)
                radial.setColorAt(1, QColor(0, 0, 0, 0))
                painter.setBrush(radial)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPointF(start_x + kw / 2, base_y + kh / 2), kw * spread, kw * spread)

            for p in k.particles:
                pc = QColor(
                    color if not cfg.data["enable_rainbow"] else QColor.fromHsv(int(self.rainbow_hue), 255, 255))
                pc.setAlpha(int(p.life * 255))
                painter.setBrush(pc)
                painter.setPen(Qt.NoPen)
                self.draw_particle(painter, p)

            painter.save()
            painter.translate(start_x + kw / 2 + k.shake_offset.x(), base_y + kh / 2 + k.shake_offset.y())
            painter.scale(k.curr_scale, k.curr_scale)
            painter.rotate(k.rotation)

            if cfg.data["border_glow"] and k.is_pressed:
                painter.setPen(QPen(color.lighter(150), cfg.data["border_width"] * 2))
            else:
                painter.setPen(QPen(color, cfg.data["border_width"]))

            fill = QColor(color).lighter(60) if k.is_pressed else QColor(20, 20, 20, 220)
            painter.setBrush(fill)

            rect = QRectF(-kw / 2, -kh / 2, kw, kh)
            self.draw_key_shape(painter, rect, cfg.data["key_shape"])

            painter.setPen(Qt.white)
            painter.setFont(QFont("Microsoft JhengHei UI", int(kh * 0.3), QFont.Bold))
            painter.drawText(rect, Qt.AlignCenter, k.label.upper())

            if cfg.data["show_key_count"] or (cfg.data["enable_combo"] and k.combo > 1):
                painter.setFont(QFont("Microsoft JhengHei UI", cfg.data["key_count_font_size"], QFont.Bold))
                count_rect = QRectF(-kw / 2, kh / 2 - 20, kw, 20)

                display_text = ""
                if cfg.data["show_key_count"]:
                    painter.setPen(QColor(cfg.data["key_count_color"]))
                    display_text = str(k.press_count)

                if cfg.data["enable_combo"] and k.combo > 1:
                    if display_text:
                        display_text += f" ({t('combo_display').format(k.combo)})"
                    else:
                        painter.setPen(Qt.white)
                        display_text = t('combo_display').format(k.combo)

                painter.drawText(count_rect, Qt.AlignCenter, display_text)

            painter.restore()

    def get_key_at_pos(self, pos):
        """獲取點擊位置對應的按鍵索引"""
        kw, kh = cfg.data["width"], cfg.data["height"]

        for idx in range(len(self.keys_state)):
            x, y = self.get_key_position(idx)
            # 擴大hitbox便於點擊
            if (x - 10 <= pos.x() <= x + kw + 10 and
                    y - 10 <= pos.y() <= y + kh + 10):
                return idx
        return -1

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 左鍵：拖動整個窗口
            self.dragging_key_index = -1
            self.m_pos = e.globalPosition().toPoint()
        elif e.button() == Qt.RightButton:
            # 右鍵：拖動單個按鍵
            key_idx = self.get_key_at_pos(e.position())
            if key_idx >= 0:
                cfg.data["use_custom_positions"] = True
                self.dragging_key_index = key_idx
                self.drag_start_pos = e.position()

    def mouseMoveEvent(self, e):
        if self.dragging_key_index == -1:
            # 拖動整個窗口
            self.move(self.pos() + e.globalPosition().toPoint() - self.m_pos)
            self.m_pos = e.globalPosition().toPoint()
            cfg.data["window_x"] = self.pos().x()
            cfg.data["window_y"] = self.pos().y()
        elif self.dragging_key_index >= 0:
            # 拖動單個按鍵
            delta = e.position() - self.drag_start_pos
            if self.dragging_key_index < len(cfg.data["key_custom_positions"]):
                cfg.data["key_custom_positions"][self.dragging_key_index]["x"] += delta.x()
                cfg.data["key_custom_positions"][self.dragging_key_index]["y"] += delta.y()
                self.drag_start_pos = e.position()
                self.update()

    def mouseReleaseEvent(self, e):
        if self.dragging_key_index >= 0:
            cfg.save()
        self.dragging_key_index = -1

    def closeEvent(self, event):
        cfg.save()
        event.accept()


class KeybindButton(QPushButton):
    keybind_set = Signal(str)

    def __init__(self, current_key, parent=None):
        super().__init__(parent)
        self.current_key = current_key
        self.listening = False
        self.hook_id = None
        self.update_text()
        self.clicked.connect(self.start_listening)

    def update_text(self):
        if self.listening:
            self.setText(t("press_key"))
            self.setStyleSheet("background: #555; color: white; font-weight: bold; padding: 5px; min-width: 60px;")
        else:
            self.setText(self.current_key.upper())
            self.setStyleSheet("background: #555; color: white; font-weight: bold; padding: 5px; min-width: 60px;")

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.update_text()
            self.hook_id = keyboard.on_press(self.on_key_press)

    def on_key_press(self, e):
        if self.listening:
            keyboard.unhook(self.hook_id)
            self.current_key = e.name
            self.listening = False
            self.update_text()
            self.keybind_set.emit(e.name)


class OLSettings(QWidget):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        self.setWindowTitle(t("window_title"))
        self.resize(980, 650)
        self.move(cfg.data["settings_x"], cfg.data["settings_y"])

        main_lay = QVBoxLayout(self)
        self.tabs = QTabWidget()
        main_lay.addWidget(self.tabs)

        self.create_all_tabs()

        self.save_btn = QPushButton(t("save_button"))
        self.save_btn.setStyleSheet("""
            height: 50px; 
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5A5A5A, stop:1 #3A3A3A);
            color: white; font-weight: bold; font-size: 14px; font-family: 'Microsoft JhengHei UI';
            border: 2px solid #707070; border-radius: 8px;
        """)
        self.save_btn.clicked.connect(self.save_all_animated)
        main_lay.addWidget(self.save_btn)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size: 12px;")
        main_lay.addWidget(self.message_label)

    def on_language_changed(self, index):
        if not hasattr(self, 'language_codes') or index >= len(self.language_codes):
            return

        new_lang = self.language_codes[index]
        old_lang = cfg.data.get("language", "zh_TW")

        if new_lang != old_lang:
            cfg.data["language"] = new_lang
            translation_manager.set_language(new_lang)
            cfg.save()

            pos = self.pos()
            was_visible = self.isVisible()

            current_tab_index = self.tabs.currentIndex()

            def rebuild_ui():
                while self.tabs.count() > 0:
                    self.tabs.removeTab(0)
                self.create_all_tabs()
                self.setWindowTitle(t("window_title"))
                self.save_btn.setText(t("save_button"))

                if current_tab_index < self.tabs.count():
                    self.tabs.setCurrentIndex(current_tab_index)

                if was_visible:
                    self.show()
                    self.raise_()
                    self.activateWindow()

            QTimer.singleShot(100, rebuild_ui)

    def create_all_tabs(self):
        # Tab 1: Layout
        self.t_lay = QWidget()
        lay_main_layout = QVBoxLayout(self.t_lay)

        # 尺寸設定群組
        size_group = QGroupBox(t("size_group"))
        lf = QFormLayout()
        self.ui_w = self.add_spin(lf, t("key_width"), 30, 5000, cfg.data["width"])
        self.ui_h = self.add_spin(lf, t("key_height"), 20, 5000, cfg.data["height"])
        self.ui_spacing = self.add_spin(lf, t("key_spacing"), 0, 500, cfg.data["spacing"])
        self.ui_bg_opacity = self.add_slider(lf, t("bg_opacity"), 0, 255, cfg.data["background_opacity"])

        self.ui_w.valueChanged.connect(self.auto_apply)
        self.ui_h.valueChanged.connect(self.auto_apply)
        self.ui_spacing.valueChanged.connect(self.auto_apply)
        self.ui_bg_opacity.valueChanged.connect(self.auto_apply)
        size_group.setLayout(lf)
        lay_main_layout.addWidget(size_group)

        # 位置設定群組
        position_group = QGroupBox(t("position_group"))
        pf = QFormLayout()
        reset_positions_btn = QPushButton(t("reset_key_positions"))
        reset_positions_btn.setStyleSheet("background: #4A90E2; color: white; padding: 8px; font-weight: bold;")
        reset_positions_btn.clicked.connect(self.reset_key_positions)
        pf.addRow(reset_positions_btn)

        position_note = QLabel(t("position_note"))
        position_note.setStyleSheet("color: #888; font-size: 12px;")
        position_note.setWordWrap(True)
        pf.addRow(position_note)
        position_group.setLayout(pf)
        lay_main_layout.addWidget(position_group)

        lay_main_layout.addStretch()
        self.tabs.addTab(self.t_lay, t("tab_layout"))

        # Tab 2: KPS Settings
        self.t_kps = QWidget()
        kps_main_layout = QVBoxLayout(self.t_kps)

        kps_group = QGroupBox(t("kps_display_group"))
        kps_f = QFormLayout()
        self.ui_show_kps = self.add_check(kps_f, t("show_kps"), cfg.data["show_kps"])
        self.ui_kps_size = self.add_spin(kps_f, t("kps_font_size"), 10, 500, cfg.data["kps_font_size"])
        self.ui_kps_x = self.add_spin(kps_f, t("kps_x_offset"), -10000, 10000, cfg.data["kps_pos_x"])
        self.ui_kps_y = self.add_spin(kps_f, t("kps_y_offset"), -10000, 10000, cfg.data["kps_pos_y"])
        self.ui_kps_max = self.add_spin(kps_f, t("max_kps_limit"), 1, 1000, cfg.data["max_kps"])
        self.ui_kps_color_change = self.add_check(kps_f, t("kps_color_change"), cfg.data["kps_color_change"])

        self.ui_show_kps.stateChanged.connect(self.auto_apply)
        self.ui_kps_size.valueChanged.connect(self.auto_apply)
        self.ui_kps_x.valueChanged.connect(self.auto_apply)
        self.ui_kps_y.valueChanged.connect(self.auto_apply)
        self.ui_kps_max.valueChanged.connect(self.auto_apply)
        self.ui_kps_color_change.stateChanged.connect(self.auto_apply)

        kps_color_layout = QHBoxLayout()
        kps_color_layout.addWidget(QLabel(t("kps_custom_color")))
        self.ui_kps_color_btn = QPushButton(t("choose_color"))
        self.ui_kps_color_btn.setFixedHeight(30)
        self.ui_kps_color = cfg.data["kps_custom_color"]
        self.ui_kps_color_btn.setStyleSheet(
            f"background: {self.ui_kps_color}; color: white; font-weight: bold; border: 2px solid #333;")
        self.ui_kps_color_btn.clicked.connect(self.pick_kps_color)
        kps_color_layout.addWidget(self.ui_kps_color_btn)
        kps_f.addRow(kps_color_layout)
        kps_f.addRow(QLabel(t("kps_color_note")))

        kps_group.setLayout(kps_f)
        kps_main_layout.addWidget(kps_group)

        max_kps_group = QGroupBox(t("max_kps_group"))
        max_kps_f = QFormLayout()
        self.ui_show_max_kps = self.add_check(max_kps_f, t("show_max_kps"), cfg.data["show_max_kps"])
        self.ui_max_kps_x = self.add_spin(max_kps_f, t("max_kps_x_offset"), -10000, 10000, cfg.data["max_kps_pos_x"])
        self.ui_max_kps_y = self.add_spin(max_kps_f, t("max_kps_y_offset"), -10000, 10000, cfg.data["max_kps_pos_y"])
        self.ui_auto_switch = self.add_check(max_kps_f, t("auto_switch_max"), cfg.data["auto_switch_max"])
        self.ui_switch_delay = self.add_dspin(max_kps_f, t("switch_delay"), 1.0, 30.0, cfg.data["switch_delay"])
        max_kps_f.addRow(QLabel(t("switch_note")))

        self.ui_show_max_kps.stateChanged.connect(self.auto_apply)
        self.ui_max_kps_x.valueChanged.connect(self.auto_apply)
        self.ui_max_kps_y.valueChanged.connect(self.auto_apply)
        self.ui_auto_switch.stateChanged.connect(self.auto_apply)
        self.ui_switch_delay.valueChanged.connect(self.auto_apply)

        max_kps_color_layout = QHBoxLayout()
        max_kps_color_layout.addWidget(QLabel(t("max_kps_color")))
        self.ui_max_kps_color_btn = QPushButton(t("choose_color"))
        self.ui_max_kps_color_btn.setFixedHeight(30)
        self.ui_max_kps_color = cfg.data["max_kps_color"]
        self.ui_max_kps_color_btn.setStyleSheet(
            f"background: {self.ui_max_kps_color}; color: white; font-weight: bold; border: 2px solid #333;")
        self.ui_max_kps_color_btn.clicked.connect(self.pick_max_kps_color)
        max_kps_color_layout.addWidget(self.ui_max_kps_color_btn)
        max_kps_f.addRow(max_kps_color_layout)

        reset_max_kps_btn = QPushButton(t("reset_max_kps"))
        reset_max_kps_btn.setStyleSheet("background: #FF6B6B; color: white; padding: 8px; font-weight: bold;")
        reset_max_kps_btn.clicked.connect(self.reset_max_kps_only)
        max_kps_f.addRow(reset_max_kps_btn)

        max_kps_group.setLayout(max_kps_f)
        kps_main_layout.addWidget(max_kps_group)
        kps_main_layout.addStretch()
        self.tabs.addTab(self.t_kps, t("tab_kps"))

        # Tab 3: Effects Options
        self.t_effects_options = QWidget()
        effects_main_layout = QVBoxLayout(self.t_effects_options)

        physics_group = QGroupBox(t("physics_group"))
        pf = QFormLayout()
        self.ui_stiff = self.add_slider(pf, t("spring_stiffness"), 1, 200, cfg.data["spring_stiffness"])
        self.ui_scale = self.add_slider(pf, t("press_scale"), 10, 200, cfg.data["press_scale"])

        self.ui_stiff.valueChanged.connect(self.auto_apply)
        self.ui_scale.valueChanged.connect(self.auto_apply)

        self.ui_anim_style = QComboBox()
        anim_items = [t("anim_default"), t("anim_wave"), t("anim_pulse"), t("anim_bounce"), t("anim_elastic")]
        self.ui_anim_style.addItems(anim_items)
        anim_map = {"default": 0, "wave": 1, "pulse": 2, "bounce": 3, "elastic": 4}
        self.ui_anim_style.setCurrentIndex(anim_map.get(cfg.data["animation_style"], 0))
        self.ui_anim_style.currentIndexChanged.connect(self.auto_apply)
        pf.addRow(t("animation_style"), self.ui_anim_style)

        self.ui_key_shape = QComboBox()
        shape_items = [t("shape_rounded"), t("shape_square"), t("shape_circle"), t("shape_hexagon")]
        self.ui_key_shape.addItems(shape_items)
        shape_map = {"rounded": 0, "square": 1, "circle": 2, "hexagon": 3}
        self.ui_key_shape.setCurrentIndex(shape_map.get(cfg.data["key_shape"], 0))
        self.ui_key_shape.currentIndexChanged.connect(self.auto_apply)
        pf.addRow(t("key_shape"), self.ui_key_shape)

        self.ui_rotation = self.add_slider(pf, t("rotation_angle"), 0, 360, cfg.data["rotation_on_press"])
        self.ui_border = self.add_slider(pf, t("border_width"), 1, 20, cfg.data["border_width"])
        self.ui_border_glow = self.add_check(pf, t("border_glow"), cfg.data["border_glow"])

        self.ui_rotation.valueChanged.connect(self.auto_apply)
        self.ui_border.valueChanged.connect(self.auto_apply)
        self.ui_border_glow.stateChanged.connect(self.auto_apply)

        physics_group.setLayout(pf)
        effects_main_layout.addWidget(physics_group)

        particle_group = QGroupBox(t("particle_group"))
        paf = QFormLayout()
        self.ui_part_en = self.add_check(paf, t("enable_particles"), cfg.data["enable_part"])
        self.ui_part_c = self.add_spin(paf, t("particle_count"), 0, 200, cfg.data["part_count"])
        self.ui_part_g = self.add_slider(paf, t("gravity"), 0, 500, cfg.data["part_gravity"])
        self.ui_part_f = self.add_slider(paf, t("explosion_force"), 10, 500, cfg.data["part_force"])
        self.ui_part_d = self.add_slider(paf, t("decay_speed"), 1, 200, cfg.data["part_decay"])

        self.ui_part_en.stateChanged.connect(self.auto_apply)
        self.ui_part_c.valueChanged.connect(self.auto_apply)
        self.ui_part_g.valueChanged.connect(self.auto_apply)
        self.ui_part_f.valueChanged.connect(self.auto_apply)
        self.ui_part_d.valueChanged.connect(self.auto_apply)

        self.ui_part_shape = QComboBox()
        part_shape_items = [t("particle_circle"), t("particle_square"), t("particle_star")]
        self.ui_part_shape.addItems(part_shape_items)
        part_shape_map = {"circle": 0, "square": 1, "star": 2}
        self.ui_part_shape.setCurrentIndex(part_shape_map.get(cfg.data["particle_shape"], 0))
        self.ui_part_shape.currentIndexChanged.connect(self.auto_apply)
        paf.addRow(t("particle_shape"), self.ui_part_shape)

        self.ui_part_size_min = self.add_dspin(paf, t("min_particle_size"), 0.5, 50, cfg.data["particle_size_min"])
        self.ui_part_size_max = self.add_dspin(paf, t("max_particle_size"), 0.5, 50, cfg.data["particle_size_max"])

        self.ui_part_size_min.valueChanged.connect(self.auto_apply)
        self.ui_part_size_max.valueChanged.connect(self.auto_apply)

        particle_group.setLayout(paf)
        effects_main_layout.addWidget(particle_group)
        effects_main_layout.addStretch()
        self.tabs.addTab(self.t_effects_options, t("tab_effects_options"))

        # Tab 4: Visual Effects
        self.t_fx = QWidget()
        ff = QFormLayout(self.t_fx)

        glow_group = QGroupBox(t("glow_group"))
        glow_layout = QFormLayout()
        self.ui_glow_en = self.add_check(glow_layout, t("enable_glow"), cfg.data["enable_glow"])
        self.ui_glow_s = self.add_slider(glow_layout, t("glow_spread"), 5, 200, cfg.data["glow_spread"])
        self.ui_glow_i = self.add_slider(glow_layout, t("glow_intensity"), 0, 500, cfg.data["glow_intensity"])
        self.ui_glow_d = self.add_slider(glow_layout, t("glow_cooldown"), 1, 100, cfg.data["glow_decay"])

        self.ui_glow_en.stateChanged.connect(self.auto_apply)
        self.ui_glow_s.valueChanged.connect(self.auto_apply)
        self.ui_glow_i.valueChanged.connect(self.auto_apply)
        self.ui_glow_d.valueChanged.connect(self.auto_apply)

        self.ui_glow_mode = QComboBox()
        glow_mode_items = [t("glow_key"), t("glow_white"), t("glow_rainbow"), t("glow_custom")]
        self.ui_glow_mode.addItems(glow_mode_items)
        glow_mode_map = {"key": 0, "white": 1, "rainbow": 2, "custom": 3}
        self.ui_glow_mode.setCurrentIndex(glow_mode_map.get(cfg.data["glow_color_mode"], 0))
        self.ui_glow_mode.currentIndexChanged.connect(self.auto_apply)
        glow_layout.addRow(t("glow_color"), self.ui_glow_mode)

        glow_custom_layout = QHBoxLayout()
        glow_custom_layout.addWidget(QLabel(t("glow_custom_color")))
        self.ui_glow_custom_btn = QPushButton(t("choose_color"))
        self.ui_glow_custom_btn.setFixedHeight(30)
        if "glow_custom_color" not in cfg.data:
            cfg.data["glow_custom_color"] = "#FF0099"
        self.ui_glow_custom_color = cfg.data["glow_custom_color"]
        self.ui_glow_custom_btn.setStyleSheet(
            f"background: {self.ui_glow_custom_color}; color: white; font-weight: bold; border: 2px solid #333;")
        self.ui_glow_custom_btn.clicked.connect(self.pick_glow_custom_color)
        glow_custom_layout.addWidget(self.ui_glow_custom_btn)

        self.glow_custom_widget = QWidget()
        self.glow_custom_widget.setLayout(glow_custom_layout)
        glow_layout.addRow(self.glow_custom_widget)
        self.glow_custom_widget.setVisible(cfg.data["glow_color_mode"] == "custom")
        self.ui_glow_mode.currentIndexChanged.connect(self.on_glow_mode_changed)

        glow_group.setLayout(glow_layout)
        ff.addRow(glow_group)

        vis_group = QGroupBox(t("vis_group"))
        vis_layout = QFormLayout()
        self.ui_vis_en = self.add_check(vis_layout, t("enable_vis"), cfg.data["enable_vis"])
        self.ui_vis_h = self.add_spin(vis_layout, t("vis_height"), 100, 5000, cfg.data["vis_height"])
        self.ui_vis_s = self.add_slider(vis_layout, t("note_speed"), 1, 100, cfg.data["vis_speed"])
        self.ui_vis_opacity = self.add_slider(vis_layout, t("note_opacity"), 0, 255, cfg.data["vis_opacity"])
        self.ui_vis_gradient = self.add_check(vis_layout, t("vis_gradient"), cfg.data["vis_gradient"])
        self.ui_trail_en = self.add_check(vis_layout, t("enable_trail"), cfg.data["enable_trail"])
        self.ui_trail_len = self.add_slider(vis_layout, t("trail_length"), 1, 50, cfg.data["trail_length"])

        self.ui_vis_en.stateChanged.connect(self.auto_apply)
        self.ui_vis_h.valueChanged.connect(self.auto_apply)
        self.ui_vis_s.valueChanged.connect(self.auto_apply)
        self.ui_vis_opacity.valueChanged.connect(self.auto_apply)
        self.ui_vis_gradient.stateChanged.connect(self.auto_apply)
        self.ui_trail_en.stateChanged.connect(self.auto_apply)
        self.ui_trail_len.valueChanged.connect(self.auto_apply)

        vis_group.setLayout(vis_layout)
        ff.addRow(vis_group)

        rainbow_group = QGroupBox(t("enable_rainbow"))
        rainbow_layout = QFormLayout()
        self.ui_rainbow_en = self.add_check(rainbow_layout, t("enable_rainbow"), cfg.data["enable_rainbow"])
        self.ui_rainbow_speed = self.add_slider(rainbow_layout, t("rainbow_speed"), 1, 100, cfg.data["rainbow_speed"])

        self.ui_rainbow_en.stateChanged.connect(self.auto_apply)
        self.ui_rainbow_speed.valueChanged.connect(self.auto_apply)

        rainbow_layout.addRow(QLabel(t("rainbow_note")))
        rainbow_group.setLayout(rainbow_layout)
        ff.addRow(rainbow_group)

        self.ui_shake_en = self.add_check(ff, t("enable_shake"), cfg.data["enable_shake"])
        self.ui_shake_int = self.add_slider(ff, t("shake_intensity"), 1, 100, cfg.data["shake_intensity"])

        self.ui_shake_en.stateChanged.connect(self.auto_apply)
        self.ui_shake_int.valueChanged.connect(self.auto_apply)

        self.tabs.addTab(self.t_fx, t("tab_effects"))

        # Tab 5: Combo & Stats
        self.t_combo = QWidget()
        combo_main_layout = QVBoxLayout(self.t_combo)

        # 連擊設定群組
        combo_group = QGroupBox(t("combo_group"))
        combof = QFormLayout()
        self.ui_combo_en = self.add_check(combof, t("enable_combo"), cfg.data["enable_combo"])
        self.ui_combo_reset = self.add_dspin(combof, t("combo_reset_time"), 0.1, 10, cfg.data["combo_reset_time"])

        self.ui_combo_en.stateChanged.connect(self.auto_apply)
        self.ui_combo_reset.valueChanged.connect(self.auto_apply)
        combo_group.setLayout(combof)
        combo_main_layout.addWidget(combo_group)

        # 統計顯示群組
        stats_group = QGroupBox(t("stats_group"))
        statsf = QFormLayout()
        self.ui_stats_en = self.add_check(statsf, t("enable_stats"), cfg.data["enable_stats"])
        self.ui_stats_en.stateChanged.connect(self.auto_apply)

        self.stats_label = QLabel(t("total_presses").format(cfg.data['total_presses']))
        statsf.addRow(self.stats_label)

        reset_btn = QPushButton(t("reset_all_stats"))
        reset_btn.setStyleSheet("background: #FF6B6B; color: white; padding: 8px; font-weight: bold;")
        reset_btn.clicked.connect(self.reset_stats)
        statsf.addRow(reset_btn)
        stats_group.setLayout(statsf)
        combo_main_layout.addWidget(stats_group)

        # 按鍵計數顯示群組
        key_count_group = QGroupBox(t("key_count_group"))
        kcf = QFormLayout()
        self.ui_show_key_count = self.add_check(kcf, t("show_key_count"), cfg.data["show_key_count"])
        self.ui_key_count_size = self.add_spin(kcf, t("key_count_font"), 8, 30, cfg.data["key_count_font_size"])

        self.ui_show_key_count.stateChanged.connect(self.auto_apply)
        self.ui_key_count_size.valueChanged.connect(self.auto_apply)

        key_count_color_layout = QHBoxLayout()
        key_count_color_layout.addWidget(QLabel(t("key_count_color")))
        self.ui_key_count_color_btn = QPushButton(t("choose_color"))
        self.ui_key_count_color_btn.setFixedHeight(30)
        self.ui_key_count_color = cfg.data["key_count_color"]
        self.ui_key_count_color_btn.setStyleSheet(
            f"background: {self.ui_key_count_color}; color: white; font-weight: bold; border: 2px solid #333;")
        self.ui_key_count_color_btn.clicked.connect(self.pick_key_count_color)
        key_count_color_layout.addWidget(self.ui_key_count_color_btn)
        kcf.addRow(key_count_color_layout)
        key_count_group.setLayout(kcf)
        combo_main_layout.addWidget(key_count_group)

        combo_main_layout.addStretch()
        self.tabs.addTab(self.t_combo, t("tab_combo"))

        # Tab 6: Key Settings
        self.t_keys = QWidget()
        keys_main_layout = QVBoxLayout(self.t_keys)

        # 按鍵數量設定群組
        count_group = QGroupBox(t("key_count_group"))
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel(t("key_count")))
        self.ui_cnt = QSpinBox()
        self.ui_cnt.setRange(1, 20)
        self.ui_cnt.setValue(cfg.data["key_count"])
        self.ui_cnt.valueChanged.connect(self.on_key_count_changed)
        count_layout.addWidget(self.ui_cnt)
        count_layout.addStretch()
        count_group.setLayout(count_layout)
        keys_main_layout.addWidget(count_group)

        # 按鍵配置群組
        keys_config_group = QGroupBox(t("keys_config_group"))
        keys_config_layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.keys_container = QWidget()
        self.k_list_v = QVBoxLayout(self.keys_container)
        self.k_list_v.setSpacing(8)
        scroll.setWidget(self.keys_container)

        keys_config_layout.addWidget(scroll)
        keys_config_group.setLayout(keys_config_layout)
        keys_main_layout.addWidget(keys_config_group)

        self.tabs.addTab(self.t_keys, t("tab_keys"))
        self.draw_key_list()

        # Tab 7: Window Settings
        self.t_window = QWidget()
        window_main_layout = QVBoxLayout(self.t_window)

        adv_group = QGroupBox(t("tab_advanced"))
        advf = QFormLayout()
        self.ui_fps = self.add_spin(advf, t("fps_limit"), 30, 500, cfg.data["fps_limit"])
        self.ui_fps.valueChanged.connect(self.auto_apply)
        advf.addRow(QLabel(t("fps_note")))
        adv_group.setLayout(advf)
        window_main_layout.addWidget(adv_group)

        keybinds_group = QGroupBox(t("tab_keybinds"))
        keybinds_f = QFormLayout()
        keybinds_f.addRow(QLabel(t("keybind_note")))
        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(QLabel(t("toggle_settings")))
        self.ui_toggle_key = KeybindButton(cfg.data["toggle_settings_key"])
        self.ui_toggle_key.keybind_set.connect(self.on_toggle_keybind_set)
        toggle_layout.addWidget(self.ui_toggle_key)
        toggle_layout.addStretch()
        keybinds_f.addRow(toggle_layout)
        keybinds_group.setLayout(keybinds_f)
        window_main_layout.addWidget(keybinds_group)

        lang_group = QGroupBox(t("tab_language"))
        langf = QFormLayout()

        self.ui_language = QComboBox()
        self.language_codes = []
        available_langs = translation_manager.get_available_languages()
        current_lang = cfg.data.get("language", "zh_TW")
        current_index = 0

        for idx, (code, name) in enumerate(available_langs):
            self.ui_language.addItem(name)
            self.language_codes.append(code)
            if code == current_lang:
                current_index = idx

        self.ui_language.setCurrentIndex(current_index)
        self.ui_language.currentIndexChanged.connect(self.on_language_changed)

        langf.addRow(t("language"), self.ui_language)
        langf.addRow(QLabel(t("language_note")))

        lang_info = QLabel(f"languages/{current_lang}.json")
        lang_info.setStyleSheet("color: #888; font-size: 10px;")
        langf.addRow(lang_info)

        lang_group.setLayout(langf)
        window_main_layout.addWidget(lang_group)
        window_main_layout.addStretch()
        self.tabs.addTab(self.t_window, t("tab_window"))

    def on_glow_mode_changed(self, index):
        self.glow_custom_widget.setVisible(index == 3)
        self.auto_apply()

    def pick_glow_custom_color(self):
        res = QColorDialog.getColor(QColor(self.ui_glow_custom_color))
        if res.isValid():
            self.ui_glow_custom_color = res.name()
            self.ui_glow_custom_btn.setStyleSheet(
                f"background: {res.name()}; color: white; font-weight: bold; border: 2px solid #333;")
            self.auto_apply()

    def on_toggle_keybind_set(self, key):
        cfg.data["toggle_settings_key"] = key
        self.auto_apply()

    def on_key_count_changed(self, new_count):
        """處理按鍵數量變化"""
        old_count = cfg.data["key_count"]

        # 修復3: 正確調整配置數組
        # 調整 keys 數組
        while len(cfg.data["keys"]) < new_count:
            cfg.data["keys"].append("k")
        if len(cfg.data["keys"]) > new_count:
            cfg.data["keys"] = cfg.data["keys"][:new_count]

        # 調整 colors 數組
        default_colors = ["#00E5FF", "#00FF88", "#FF0077", "#FFD600", "#9C27B0", "#FF5722"]
        while len(cfg.data["colors"]) < new_count:
            idx = len(cfg.data["colors"])
            cfg.data["colors"].append(default_colors[idx % len(default_colors)])
        if len(cfg.data["colors"]) > new_count:
            cfg.data["colors"] = cfg.data["colors"][:new_count]

        # 調整自定義位置數組
        while len(cfg.data["key_custom_positions"]) < new_count:
            cfg.data["key_custom_positions"].append({"x": 0, "y": 0})
        if len(cfg.data["key_custom_positions"]) > new_count:
            cfg.data["key_custom_positions"] = cfg.data["key_custom_positions"][:new_count]

        # 重要：立即重新繪製按鍵列表以反映數量變化
        self.draw_key_list()
        self.auto_apply()

    def reset_key_positions(self):
        """重置按鍵位置為水平對齊"""
        cfg.data["use_custom_positions"] = False
        cfg.data["key_custom_positions"] = [{"x": 0, "y": 0} for _ in range(cfg.data["key_count"])]
        cfg.save()
        self.overlay.update()
        self.show_message(t("positions_reset"))

    def auto_apply(self):
        anim_reverse = ["default", "wave", "pulse", "bounce", "elastic"]
        shape_reverse = ["rounded", "square", "circle", "hexagon"]
        part_shape_reverse = ["circle", "square", "star"]

        cfg.data.update({
            "width": self.ui_w.value(),
            "height": self.ui_h.value(),
            "spacing": self.ui_spacing.value(),
            "background_opacity": self.ui_bg_opacity.value(),
            "show_kps": self.ui_show_kps.isChecked(),
            "kps_font_size": self.ui_kps_size.value(),
            "kps_pos_x": self.ui_kps_x.value(),
            "kps_pos_y": self.ui_kps_y.value(),
            "max_kps": self.ui_kps_max.value(),
            "kps_color_change": self.ui_kps_color_change.isChecked(),
            "kps_custom_color": self.ui_kps_color,
            "show_max_kps": self.ui_show_max_kps.isChecked(),
            "max_kps_pos_x": self.ui_max_kps_x.value(),
            "max_kps_pos_y": self.ui_max_kps_y.value(),
            "max_kps_color": self.ui_max_kps_color,
            "spring_stiffness": self.ui_stiff.value(),
            "press_scale": self.ui_scale.value(),
            "animation_style": anim_reverse[self.ui_anim_style.currentIndex()],
            "key_shape": shape_reverse[self.ui_key_shape.currentIndex()],
            "rotation_on_press": self.ui_rotation.value(),
            "border_width": self.ui_border.value(),
            "border_glow": self.ui_border_glow.isChecked(),
            "enable_part": self.ui_part_en.isChecked(),
            "part_count": self.ui_part_c.value(),
            "part_gravity": self.ui_part_g.value(),
            "part_force": self.ui_part_f.value(),
            "part_decay": self.ui_part_d.value(),
            "particle_shape": part_shape_reverse[self.ui_part_shape.currentIndex()],
            "particle_size_min": self.ui_part_size_min.value(),
            "particle_size_max": self.ui_part_size_max.value(),
            "enable_glow": self.ui_glow_en.isChecked(),
            "glow_spread": self.ui_glow_s.value(),
            "glow_intensity": self.ui_glow_i.value(),
            "glow_decay": self.ui_glow_d.value(),
            "glow_color_mode": ["key", "white", "rainbow", "custom"][self.ui_glow_mode.currentIndex()],
            "glow_custom_color": self.ui_glow_custom_color,
            "enable_vis": self.ui_vis_en.isChecked(),
            "vis_height": self.ui_vis_h.value(),
            "vis_speed": self.ui_vis_s.value(),
            "vis_opacity": self.ui_vis_opacity.value(),
            "vis_gradient": self.ui_vis_gradient.isChecked(),
            "enable_rainbow": self.ui_rainbow_en.isChecked(),
            "rainbow_speed": self.ui_rainbow_speed.value(),
            "enable_trail": self.ui_trail_en.isChecked(),
            "trail_length": self.ui_trail_len.value(),
            "enable_shake": self.ui_shake_en.isChecked(),
            "shake_intensity": self.ui_shake_int.value(),
            "enable_combo": self.ui_combo_en.isChecked(),
            "combo_reset_time": self.ui_combo_reset.value(),
            "enable_stats": self.ui_stats_en.isChecked(),
            "fps_limit": self.ui_fps.value(),
            "key_count": self.ui_cnt.value(),
            "keys": [btn.current_key for btn in self.keybind_buttons] if hasattr(self, 'keybind_buttons') else cfg.data[
                "keys"],
            "colors": self.cls if hasattr(self, 'cls') else cfg.data["colors"],
            "show_key_count": self.ui_show_key_count.isChecked(),
            "key_count_font_size": self.ui_key_count_size.value(),
            "key_count_color": self.ui_key_count_color,
            "auto_switch_max": self.ui_auto_switch.isChecked(),
            "switch_delay": self.ui_switch_delay.value(),
        })

        self.overlay.setup_ui()
        self.overlay.timer.setInterval(int(1000 / cfg.data["fps_limit"]))

    def add_spin(self, f, l, mn, mx, v):
        s = QSpinBox()
        s.setRange(mn, mx)
        s.setValue(v)
        f.addRow(l, s)
        return s

    def add_dspin(self, f, l, mn, mx, v):
        s = QDoubleSpinBox()
        s.setRange(mn, mx)
        s.setValue(v)
        s.setSingleStep(0.1)
        f.addRow(l, s)
        return s

    def add_slider(self, f, l, mn, mx, v):
        h = QHBoxLayout()
        s = QSlider(Qt.Horizontal)
        s.setRange(mn, mx)
        s.setValue(v)
        label = QLabel(str(v))
        label.setMinimumWidth(40)
        label.setAlignment(Qt.AlignRight)
        s.valueChanged.connect(lambda val: label.setText(str(val)))
        h.addWidget(s, 1)
        h.addWidget(label, 0)
        f.addRow(l, h)
        return s

    def add_check(self, f, l, v):
        c = QCheckBox(l)
        c.setChecked(v)
        f.addRow(c)
        return c

    def draw_key_list(self):
        while self.k_list_v.count():
            i = self.k_list_v.takeAt(0)
            if i.widget():
                i.widget().deleteLater()

        self.keybind_buttons = []
        self.cls = []

        # 修復1: 使用當前設定的按鍵數量，而不是配置中的數量
        current_key_count = self.ui_cnt.value()

        for i in range(current_key_count):
            r = QHBoxLayout()
            r.setSpacing(8)

            label = QLabel(t("key_label").format(i + 1))
            label.setMinimumWidth(60)

            current_key = cfg.data["keys"][i] if i < len(cfg.data["keys"]) else "k"
            keybind_btn = KeybindButton(current_key)
            keybind_btn.keybind_set.connect(self.auto_apply)
            self.keybind_buttons.append(keybind_btn)

            c = cfg.data["colors"][i] if i < len(cfg.data["colors"]) else "#FFFFFF"
            b = QPushButton(t("choose_color"))
            b.setFixedHeight(30)
            b.setStyleSheet(f"background: {c}; color: white; font-weight: bold; border: 2px solid #333;")
            b.clicked.connect(lambda ch, idx=i, btn=b: self.pick_c(idx, btn))

            r.addWidget(label)
            r.addWidget(keybind_btn)
            r.addWidget(b, 1)

            self.k_list_v.addLayout(r)
            self.cls.append(c)

        self.k_list_v.addStretch()

    def pick_key_count_color(self):
        res = QColorDialog.getColor(QColor(self.ui_key_count_color))
        if res.isValid():
            self.ui_key_count_color = res.name()
            self.ui_key_count_color_btn.setStyleSheet(
                f"background: {res.name()}; color: white; font-weight: bold; border: 2px solid #333;")
            self.auto_apply()

    def pick_c(self, idx, btn):
        res = QColorDialog.getColor(QColor(self.cls[idx]))
        if res.isValid():
            self.cls[idx] = res.name()
            btn.setStyleSheet(f"background: {res.name()}; color: white; font-weight: bold; border: 2px solid #333;")
            self.auto_apply()

    def pick_kps_color(self):
        res = QColorDialog.getColor(QColor(self.ui_kps_color))
        if res.isValid():
            self.ui_kps_color = res.name()
            self.ui_kps_color_btn.setStyleSheet(
                f"background: {res.name()}; color: white; font-weight: bold; border: 2px solid #333;")
            self.auto_apply()

    def pick_max_kps_color(self):
        res = QColorDialog.getColor(QColor(self.ui_max_kps_color))
        if res.isValid():
            self.ui_max_kps_color = res.name()
            self.ui_max_kps_color_btn.setStyleSheet(
                f"background: {res.name()}; color: white; font-weight: bold; border: 2px solid #333;")
            self.auto_apply()

    def reset_stats(self):
        cfg.data["total_presses"] = 0
        cfg.data["session_start"] = time.time()
        cfg.save()
        self.stats_label.setText(t("total_presses").format(0))
        self.show_message(t("stats_reset"))

    def reset_max_kps_only(self):
        cfg.data["max_kps_record"] = 0
        self.show_message(t("max_kps_reset"))

    def show_message(self, text):
        self.message_label.setText(text)
        QTimer.singleShot(3000, lambda: self.message_label.setText(""))

    def save_all_animated(self):
        self.save_btn.setEnabled(False)

        pressed_style = """
            height: 50px; 
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4A4A4A, stop:1 #2A2A2A);
            color: white; font-weight: bold; font-size: 14px; font-family: 'Microsoft JhengHei UI';
            border: 2px solid #606060; border-radius: 8px;
        """

        original_style = """
            height: 50px; 
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5A5A5A, stop:1 #3A3A3A);
            color: white; font-weight: bold; font-size: 14px; font-family: 'Microsoft JhengHei UI';
            border: 2px solid #707070; border-radius: 8px;
        """

        self.save_btn.setStyleSheet(pressed_style)
        self.save_all()
        self.show_message(t("save_success"))

        QTimer.singleShot(150, lambda: self.save_btn.setStyleSheet(original_style))
        QTimer.singleShot(150, lambda: self.save_btn.setEnabled(True))

    def save_all(self):
        self.auto_apply()
        cfg.save()

    def closeEvent(self, event):
        cfg.data["settings_x"] = self.pos().x()
        cfg.data["settings_y"] = self.pos().y()
        cfg.save()
        event.accept()

    def moveEvent(self, event):
        cfg.data["settings_x"] = self.pos().x()
        cfg.data["settings_y"] = self.pos().y()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(120, 120, 120, 180))
        painter.setFont(QFont("Arial", 9))
        watermark_rect = QRectF(self.width() - 130, self.height() - 25, 120, 20)
        painter.drawText(watermark_rect, Qt.AlignRight | Qt.AlignBottom, "Made By yulun <3")


class ToggleKeybindListener(QThread):
    toggle_signal = Signal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.current_hook = None

    def run(self):
        while self.running:
            try:
                if self.current_hook is not None:
                    keyboard.unhook(self.current_hook)

                def on_toggle(e):
                    if e.event_type == keyboard.KEY_DOWN:
                        self.toggle_signal.emit()

                self.current_hook = keyboard.on_press_key(cfg.data.get("toggle_settings_key", "f1"), on_toggle)

                for _ in range(10):
                    if not self.running:
                        break
                    self.msleep(100)
            except:
                pass

    def stop(self):
        self.running = False
        if self.current_hook is not None:
            keyboard.unhook(self.current_hook)


class InputWorker(QThread):
    sig = Signal(str, bool)

    def run(self):
        def key_handler(e):
            if e.name != cfg.data.get("toggle_settings_key", "f1"):
                self.sig.emit(e.name, e.event_type == keyboard.KEY_DOWN)

        keyboard.hook(key_handler)
        while True:
            self.msleep(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft JhengHei UI", 9))

    translation_manager.set_language(cfg.data.get("language", "zh_TW"))

    splash = SplashScreen()
    splash.show()

    overlay = OLOverlay()
    worker = InputWorker()
    worker.sig.connect(overlay.handle_input)
    worker.start()

    settings = OLSettings(overlay)

    toggle_listener = ToggleKeybindListener()


    def toggle_settings_window():
        if settings.isVisible():
            settings.hide()
        else:
            settings.show()
            settings.activateWindow()


    toggle_listener.toggle_signal.connect(toggle_settings_window)
    toggle_listener.start()


    def show_main_windows():
        overlay.show()


    QTimer.singleShot(2500, settings.show)
    QTimer.singleShot(2500, show_main_windows)

    sys.exit(app.exec())
