import tkinter as tk
import math
import time
import threading
from PIL import Image, ImageTk

class TSPApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("TSP Route Planner - Branch & Bound Visualizer")
        self.root.configure(bg="#F3F4F6")

        # --- 1. Load and Dynamically Resize the Map Image ---
        try:
            pil_img = Image.open(image_path)
            screen_w = root.winfo_screenwidth()
            screen_h = root.winfo_screenheight()
            max_w = int(screen_w * 0.9)
            max_h = int(screen_h * 0.75) 
            
            pil_img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(pil_img)
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            self.bg_image = None

        # --- 2. Setup UI Controls (Top Panel - Modernized) ---
        ui_frame = tk.Frame(root, bg="#F3F4F6", pady=15)
        ui_frame.pack(fill=tk.X)

        self.solve_btn = tk.Button(ui_frame, text="Solve TSP (Enter)", command=self.solve, 
                                   bg="#3B82F6", fg="white", font=("Segoe UI", 11, "bold"), 
                                   relief=tk.FLAT, bd=0, padx=20, pady=8, cursor="hand2")
        self.solve_btn.pack(side=tk.LEFT, padx=(20, 10))

        self.clear_btn = tk.Button(ui_frame, text="Clear Map (Backspace)", command=self.clear, 
                                   bg="#EF4444", fg="white", font=("Segoe UI", 11, "bold"), 
                                   relief=tk.FLAT, bd=0, padx=20, pady=8, cursor="hand2")
        self.clear_btn.pack(side=tk.LEFT, padx=10)

        self.info_label = tk.Label(ui_frame, text="Click on the map to add cities. Press Enter to calculate.", 
                                   font=("Segoe UI", 12), bg="#F3F4F6", fg="#374151")
        self.info_label.pack(side=tk.LEFT, padx=20)

        # --- 3. Configure the Canvas (Clean Border) ---
        width = self.bg_image.width() if self.bg_image else 800
        height = self.bg_image.height() if self.bg_image else 600
        
        canvas_frame = tk.Frame(root, bg="#E5E7EB", bd=1, relief=tk.FLAT)
        canvas_frame.pack(pady=5, padx=20)
        
        self.canvas = tk.Canvas(canvas_frame, width=width, height=height, cursor="target", 
                                highlightthickness=0, bd=0, bg="white")
        self.canvas.pack()

        if self.bg_image:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        else:
            self.canvas.create_text(width // 2, height // 2, text=f"Could not load {image_path}.", font=("Segoe UI", 14))

        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Return>", self.solve)
        self.root.bind("<BackSpace>", self.clear)

        # --- 4. Setup Animation Controls (Bottom Panel - Sleek Player) ---
        anim_frame = tk.Frame(root, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        anim_frame.pack(fill=tk.X, padx=20, pady=15)
        
        anim_inner = tk.Frame(anim_frame, bg="#FFFFFF", pady=10, padx=10)
        anim_inner.pack(fill=tk.X)

        btn_style = {"font": ("Segoe UI", 10), "relief": tk.FLAT, "bd": 0, "padx": 15, "pady": 6, "cursor": "hand2"}

        self.prev_btn = tk.Button(anim_inner, text="< Prev", command=self.step_prev, state=tk.DISABLED, bg="#E5E7EB", fg="#374151", **btn_style)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.play_btn = tk.Button(anim_inner, text="Replay Animation", command=self.toggle_play, state=tk.DISABLED, bg="#10B981", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, bd=0, padx=15, pady=6, cursor="hand2")
        self.play_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(anim_inner, text="Next >", command=self.step_next, state=tk.DISABLED, bg="#E5E7EB", fg="#374151", **btn_style)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        tk.Label(anim_inner, text="Speed:", bg="#FFFFFF", font=("Segoe UI", 10), fg="#6B7280").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_scale = tk.Scale(anim_inner, from_=10, to=800, orient=tk.HORIZONTAL, length=120, showvalue=False, bg="#FFFFFF", highlightthickness=0, troughcolor="#E5E7EB", sliderrelief=tk.FLAT)
        self.speed_scale.set(150) 
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        self.anim_status_label = tk.Label(anim_inner, text="", font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#111827")
        self.anim_status_label.pack(side=tk.RIGHT, padx=10)

        # --- State Variables ---
        self.cities = []
        self.points_drawn = []
        self.anim_items = [] 
        
        self.history = []
        self.current_frame = 0
        self.is_playing = False
        self.anim_job = None
        self.is_calculating = False 

    def on_click(self, event):
        if self.is_playing or self.is_calculating: return 

        x, y = event.x, event.y
        self.cities.append((x, y))
        r = 7

        pt = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#EF4444", outline="#FFFFFF", width=2)
        txt = self.canvas.create_text(x, y - 16, text=str(len(self.cities)-1), font=("Segoe UI", 11, "bold"), fill="#111827")
        self.points_drawn.extend([pt, txt])
        
        self.info_label.config(text=f"Added city. Total: {len(self.cities)}", fg="#374151")
        self.reset_animation_state()

    def clear_anim_items(self):
        for item in self.anim_items:
            self.canvas.delete(item)
        self.anim_items.clear()

    def clear(self, event=None):
        if self.is_calculating: return 
        self.reset_animation_state()
        self.cities.clear()
        for pt in self.points_drawn:
            self.canvas.delete(pt)
        self.points_drawn.clear()
        self.info_label.config(text="Map cleared. Click to add cities.", fg="#374151")
        self.anim_status_label.config(text="")

    def reset_animation_state(self):
        self.is_playing = False
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        
        self.play_btn.config(text="Replay Animation", state=tk.DISABLED, bg="#9CA3AF")
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.anim_status_label.config(text="")
        self.history.clear()
        self.clear_anim_items()

    def solve(self, event=None):
        if len(self.cities) < 3:
            self.info_label.config(text="Please add at least 3 cities to form a TSP loop.", fg="#EF4444")
            return
        
        if self.is_calculating: return 

        self.is_calculating = True
        self.solve_btn.config(state=tk.DISABLED, text="Calculating...", bg="#9CA3AF")
        self.clear_btn.config(state=tk.DISABLED, bg="#9CA3AF")
        self.reset_animation_state()
        
        n = len(self.cities)
        warning_msg = " (This might take a while!)" if n > 11 else ""
        self.info_label.config(text=f"Calculating optimal route for {n} cities... Please wait.{warning_msg}", fg="#3B82F6")
        self.root.update()

        # 使用多线程，防止复杂计算卡死界面
        threading.Thread(target=self._solve_thread_worker, daemon=True).start()

    def _solve_thread_worker(self):
        start_time = time.perf_counter()
        best_path, best_cost, visited_nodes, pruned_branches = self.branch_and_bound()
        runtime = time.perf_counter() - start_time

        # 计算完成后通知主线程更新界面
        self.root.after(0, self._on_solve_complete, best_path, best_cost, visited_nodes, pruned_branches, runtime)

    def _on_solve_complete(self, best_path, best_cost, visited_nodes, pruned_branches, runtime):
        self.is_calculating = False
        self.solve_btn.config(state=tk.NORMAL, text="Solve TSP (Enter)", bg="#3B82F6")
        self.clear_btn.config(state=tk.NORMAL, bg="#EF4444")

        if best_path:
            self.info_label.config(text=f"✅ Distance: {best_cost:.1f} px  |  Runtime: {runtime:.4f}s  |  Nodes: {visited_nodes}  |  Pruned: {pruned_branches}", fg="#10B981")
            
            self.play_btn.config(state=tk.NORMAL, bg="#10B981")
            self.next_btn.config(state=tk.NORMAL)
            self.prev_btn.config(state=tk.NORMAL)
            
            # 【关键修复】：追加真正的最终完美连线作为动画的最后一帧
            self.history.append({
                'path': best_path,
                'action': 'best',
                'current_cost': best_cost,
                'best_cost': best_cost
            })
            
            self.current_frame = len(self.history) - 1
            self.draw_frame(self.current_frame)
        else:
            self.info_label.config(text="Failed to find a path.", fg="#EF4444")

    def branch_and_bound(self):
        n = len(self.cities)
        dist = [[math.hypot(self.cities[i][0] - self.cities[j][0], self.cities[i][1] - self.cities[j][1])
                 for j in range(n)] for i in range(n)]

        best_path = None
        best_cost = float('inf')
        visited_nodes = 0
        pruned_branches = 0

        def bnb(curr_path, current_cost, visited):
            nonlocal best_path, best_cost, visited_nodes, pruned_branches
            visited_nodes += 1

            self.history.append({
                'path': curr_path[:],
                'action': 'explore',
                'current_cost': current_cost,
                'best_cost': best_cost
            })

            if len(curr_path) == n:
                final_cost = current_cost + dist[curr_path[-1]][curr_path[0]]
                if final_cost < best_cost:
                    best_cost = final_cost
                    best_path = curr_path[:] + [curr_path[0]] 
                    self.history.append({
                        'path': best_path[:],
                        'action': 'best',
                        'current_cost': final_cost,
                        'best_cost': best_cost
                    })
                return

            lb = current_cost
            for i in range(n):
                if not visited[i]:
                    min_e = float('inf')
                    for j in range(n):
                        if i != j and (not visited[j] or j == curr_path[0]):
                            min_e = min(min_e, dist[i][j])
                    if min_e != float('inf'):
                        lb += min_e

            if lb >= best_cost:
                pruned_branches += 1
                self.history.append({
                    'path': curr_path[:],
                    'action': 'prune',
                    'current_cost': lb,
                    'best_cost': best_cost
                })
                return

            last_node = curr_path[-1]
            neighbors = []
            for i in range(n):
                if not visited[i]:
                    neighbors.append((dist[last_node][i], i))
            neighbors.sort()

            for d, i in neighbors:
                visited[i] = True
                curr_path.append(i)
                bnb(curr_path, current_cost + d, visited)
                curr_path.pop()
                visited[i] = False

        visited = [False] * n
        visited[0] = True
        bnb([0], 0.0, visited)

        return best_path, best_cost, visited_nodes, pruned_branches

    def draw_frame(self, frame_idx):
        self.clear_anim_items()
        if not self.history: return
        
        state = self.history[frame_idx]
        path = state['path']
        action = state['action']
        
        if action == 'explore':
            line_color = "#9CA3AF" 
            line_width = 3
            dash_pattern = (6, 6)
            status_text = f"Exploring... Cost: {state['current_cost']:.1f}"
            self.anim_status_label.config(fg="#4B5563")
        elif action == 'prune':
            line_color = "#F87171" 
            line_width = 4
            dash_pattern = ()
            status_text = f"✂️ Pruned! Bound ({state['current_cost']:.1f}) >= Best ({state['best_cost']:.1f})"
            self.anim_status_label.config(fg="#DC2626")
        elif action == 'best':
            line_color = "#3B82F6" 
            line_width = 5
            dash_pattern = ()
            status_text = f"🏆 Optimal Route Found! Cost: {state['current_cost']:.1f}"
            self.anim_status_label.config(fg="#2563EB")

        for i in range(len(path) - 1):
            p1 = self.cities[path[i]]
            p2 = self.cities[path[i + 1]]
            
            if action == 'prune' and i == len(path) - 2:
                segment_color = "#F87171"
                segment_width = 5
            else:
                segment_color = line_color
                segment_width = line_width

            line = self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=segment_color, 
                                           width=segment_width, dash=dash_pattern, capstyle=tk.ROUND)
            self.anim_items.append(line)

        self.anim_status_label.config(text=f"[{frame_idx + 1}/{len(self.history)}] {status_text}")

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_btn.config(text="Pause", bg="#F59E0B")
            self.prev_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.DISABLED)
            if self.current_frame >= len(self.history) - 1:
                self.current_frame = 0 
            self.play_next_frame()
        else:
            self.play_btn.config(text="Replay Animation", bg="#10B981")
            self.prev_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.NORMAL)
            if self.anim_job:
                self.root.after_cancel(self.anim_job)
                self.anim_job = None

    def play_next_frame(self):
        if self.is_playing and self.current_frame < len(self.history) - 1:
            self.current_frame += 1
            self.draw_frame(self.current_frame)
            
            speed_ms = self.speed_scale.get()
            self.anim_job = self.root.after(speed_ms, self.play_next_frame)
        elif self.current_frame >= len(self.history) - 1:
            self.is_playing = False
            self.play_btn.config(text="Replay Animation", bg="#10B981")
            self.prev_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.DISABLED)

    def step_next(self):
        if self.current_frame < len(self.history) - 1:
            self.current_frame += 1
            self.draw_frame(self.current_frame)
            self.prev_btn.config(state=tk.NORMAL)
        if self.current_frame >= len(self.history) - 1:
            self.next_btn.config(state=tk.DISABLED)

    def step_prev(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.draw_frame(self.current_frame)
            self.next_btn.config(state=tk.NORMAL)
        if self.current_frame <= 0:
            self.prev_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root, "europe1.jpg")
    root.mainloop()