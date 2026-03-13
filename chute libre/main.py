import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

class FreeFallSimulator:
    def __init__(self):
        self.g = 9.81  # Accélération gravitationnelle (m/s²)
        self.dt = 0.01  # Pas de temps (s)
        self.results = {}
        self.animation_running = False
        
        # Interface graphique
        self.root = tk.Tk()
        self.root.title("🎯 Simulateur de Chute Libre - Méthodes Numériques")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_gui()
        
    def setup_gui(self):
        """Configuration de l'interface graphique"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(main_frame, text="🎯 Simulateur de Chute Libre", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame pour les paramètres
        params_frame = ttk.LabelFrame(main_frame, text="📝 Paramètres de simulation", 
                                     padding="15")
        params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Champs d'entrée
        ttk.Label(params_frame, text="Position initiale X (m):").grid(row=0, column=0, 
                                                                     sticky=tk.W, pady=5)
        self.x0_var = tk.StringVar(value="0")
        ttk.Entry(params_frame, textvariable=self.x0_var, width=10).grid(row=0, column=1, 
                                                                        sticky=tk.W, padx=10)
        
        ttk.Label(params_frame, text="Hauteur initiale Y (m):").grid(row=1, column=0, 
                                                                    sticky=tk.W, pady=5)
        self.y0_var = tk.StringVar(value="50")
        ttk.Entry(params_frame, textvariable=self.y0_var, width=10).grid(row=1, column=1, 
                                                                        sticky=tk.W, padx=10)
        
        ttk.Label(params_frame, text="Vitesse initiale Y (m/s):").grid(row=2, column=0, 
                                                                       sticky=tk.W, pady=5)
        self.vy0_var = tk.StringVar(value="0")
        ttk.Entry(params_frame, textvariable=self.vy0_var, width=10).grid(row=2, column=1, 
                                                                         sticky=tk.W, padx=10)
        
        ttk.Label(params_frame, text="Pas de temps (s):").grid(row=3, column=0, 
                                                              sticky=tk.W, pady=5)
        self.dt_var = tk.StringVar(value="0.01")
        ttk.Entry(params_frame, textvariable=self.dt_var, width=10).grid(row=3, column=1, 
                                                                        sticky=tk.W, padx=10)
        
        # Boutons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text="🚀 Lancer la Simulation", 
                  command=self.run_simulation).grid(row=0, column=0, padx=5)
        
        ttk.Button(buttons_frame, text="🎬 Animation", 
                  command=self.show_animation).grid(row=0, column=1, padx=5)
        
        ttk.Button(buttons_frame, text="📊 Graphiques", 
                  command=self.show_graphs).grid(row=0, column=2, padx=5)
        
        ttk.Button(buttons_frame, text="📈 Analyse", 
                  command=self.show_analysis).grid(row=0, column=3, padx=5)
        
        # Zone de résultats
        self.results_frame = ttk.LabelFrame(main_frame, text="📊 Résultats", padding="15")
        self.results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                               pady=10)
        
        # Zone de texte pour les résultats
        self.results_text = tk.Text(self.results_frame, height=15, width=80, 
                                   font=('Courier', 10))
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, 
                                 command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
    def log_result(self, message):
        """Ajoute un message dans la zone de résultats"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update()
        
    def get_parameters(self):
        """Récupère les paramètres de l'interface"""
        try:
            x0 = float(self.x0_var.get())
            y0 = float(self.y0_var.get())
            vy0 = float(self.vy0_var.get())
            dt = float(self.dt_var.get())
            
            if y0 <= 0:
                raise ValueError("La hauteur initiale doit être positive")
            if dt <= 0:
                raise ValueError("Le pas de temps doit être positif")
                
            return x0, y0, vy0, dt
        except ValueError as e:
            messagebox.showerror("Erreur", f"Paramètres invalides: {e}")
            return None
    
    def euler_method(self, x0, y0, vy0, dt):
        """Méthode d'Euler"""
        t, y, vy = 0, y0, vy0
        times, positions, velocities = [0], [y0], [vy0]
        
        while y > 0:
            # Mise à jour selon Euler
            y += vy * dt
            vy += -self.g * dt
            t += dt
            
            times.append(t)
            positions.append(y)
            velocities.append(vy)
            
        return np.array(times), np.array(positions), np.array(velocities)
    
    def heun_method(self, x0, y0, vy0, dt):
        """Méthode de Heun (Euler amélioré)"""
        t, y, vy = 0, y0, vy0
        times, positions, velocities = [0], [y0], [vy0]
        
        while y > 0:
            # Première estimation (Euler)
            y1 = y + vy * dt
            vy1 = vy + (-self.g) * dt
            
            # Moyenne des deux estimations
            y += (vy + vy1) * dt / 2
            vy += (-self.g + (-self.g)) * dt / 2
            t += dt
            
            times.append(t)
            positions.append(y)
            velocities.append(vy)
            
        return np.array(times), np.array(positions), np.array(velocities)
    
    def rk4_method(self, x0, y0, vy0, dt):
        """Méthode de Runge-Kutta d'ordre 4"""
        t, y, vy = 0, y0, vy0
        times, positions, velocities = [0], [y0], [vy0]
        
        while y > 0:
            # k1
            k1_y = vy
            k1_vy = -self.g
            
            # k2
            k2_y = vy + k1_vy * dt/2
            k2_vy = -self.g
            
            # k3
            k3_y = vy + k2_vy * dt/2
            k3_vy = -self.g
            
            # k4
            k4_y = vy + k3_vy * dt
            k4_vy = -self.g
            
            # Mise à jour
            y += (k1_y + 2*k2_y + 2*k3_y + k4_y) * dt / 6
            vy += (k1_vy + 2*k2_vy + 2*k3_vy + k4_vy) * dt / 6
            t += dt
            
            times.append(t)
            positions.append(y)
            velocities.append(vy)
            
        return np.array(times), np.array(positions), np.array(velocities)
    
    def analytical_solution(self, x0, y0, vy0, dt):
        """Solution analytique exacte"""
        # Temps de chute total
        if vy0 >= 0:
            t_fall = (vy0 + np.sqrt(vy0**2 + 2*self.g*y0)) / self.g
        else:
            discriminant = vy0**2 + 2*self.g*y0
            if discriminant >= 0:
                t_fall = (-vy0 + np.sqrt(discriminant)) / self.g
            else:
                t_fall = 0
        
        # Génération des points temporels
        times = np.arange(0, t_fall + dt, dt)
        positions = y0 + vy0 * times - 0.5 * self.g * times**2
        velocities = vy0 - self.g * times
        
        return times, positions, velocities
    
    def run_simulation(self):
        """Lance la simulation avec les trois méthodes"""
        params = self.get_parameters()
        if params is None:
            return
            
        x0, y0, vy0, dt = params
        self.dt = dt
        
        self.log_result("=" * 60)
        self.log_result("🚀 SIMULATION DE CHUTE LIBRE")
        self.log_result("=" * 60)
        self.log_result(f"Position initiale: ({x0:.1f}, {y0:.1f}) m")
        self.log_result(f"Vitesse initiale: {vy0:.1f} m/s")
        self.log_result(f"Pas de temps: {dt} s")
        self.log_result("")
        
        # Exécution des méthodes
        try:
            self.log_result("🔄 Calcul avec la méthode d'Euler...")
            t_euler, y_euler, vy_euler = self.euler_method(x0, y0, vy0, dt)
            
            self.log_result("🔄 Calcul avec la méthode de Heun...")
            t_heun, y_heun, vy_heun = self.heun_method(x0, y0, vy0, dt)
            
            self.log_result("🔄 Calcul avec Runge-Kutta 4...")
            t_rk4, y_rk4, vy_rk4 = self.rk4_method(x0, y0, vy0, dt)
            
            self.log_result("🔄 Calcul de la solution analytique...")
            t_anal, y_anal, vy_anal = self.analytical_solution(x0, y0, vy0, dt)
            
            # Stockage des résultats
            self.results = {
                'euler': {'t': t_euler, 'y': y_euler, 'vy': vy_euler},
                'heun': {'t': t_heun, 'y': y_heun, 'vy': vy_heun},
                'rk4': {'t': t_rk4, 'y': y_rk4, 'vy': vy_rk4},
                'analytical': {'t': t_anal, 'y': y_anal, 'vy': vy_anal}
            }
            
            self.log_result("✅ Simulation terminée!")
            self.log_result("")
            
            # Affichage des temps de chute
            self.log_result("⏱️  TEMPS DE CHUTE:")
            self.log_result(f"Euler:      {t_euler[-1]:.4f} s")
            self.log_result(f"Heun:       {t_heun[-1]:.4f} s")
            self.log_result(f"RK4:        {t_rk4[-1]:.4f} s")
            self.log_result(f"Analytique: {t_anal[-1]:.4f} s")
            
            # Calcul des erreurs
            self.calculate_errors()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la simulation: {e}")
    
    def calculate_errors(self):
        """Calcule les erreurs par rapport à la solution analytique"""
        if not self.results:
            return
            
        self.log_result("")
        self.log_result("📊 ANALYSE DES ERREURS:")
        
        t_ref = self.results['analytical']['t']
        y_ref = self.results['analytical']['y']
        
        for method in ['euler', 'heun', 'rk4']:
            t_method = self.results[method]['t']
            y_method = self.results[method]['y']
            
            # Erreur sur le temps de chute
            time_error = abs(t_method[-1] - t_ref[-1])
            
            # Erreur moyenne sur la trajectoire
            min_len = min(len(t_ref), len(t_method))
            if min_len > 1:
                y_error = np.mean(np.abs(y_method[:min_len] - y_ref[:min_len]))
            else:
                y_error = 0
                
            self.log_result(f"{method.upper():8} - Erreur temps: {time_error:.6f} s, "
                           f"Erreur moyenne position: {y_error:.6f} m")
    
    def show_animation(self):
        """Affiche l'animation de la chute"""
        if not self.results:
            messagebox.showwarning("Attention", "Veuillez d'abord lancer la simulation!")
            return
            
        # Utilisation des résultats RK4 pour l'animation
        t_data = self.results['rk4']['t']
        y_data = self.results['rk4']['y']
        vy_data = self.results['rk4']['vy']
        
        # Création de la fenêtre d'animation
        anim_window = tk.Toplevel(self.root)
        anim_window.title("🎬 Animation de la Chute Libre")
        anim_window.geometry("800x600")
        
        # Configuration matplotlib
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Graphique 1: Animation de la chute
        ax1.set_xlim(-1, 1)
        ax1.set_ylim(-2, max(y_data) + 2)
        ax1.set_xlabel('Position X (m)')
        ax1.set_ylabel('Position Y (m)')
        ax1.set_title('🎯 Animation de la Chute')
        ax1.grid(True, alpha=0.3)
        
        # Sol
        ax1.axhline(y=0, color='brown', linewidth=3, label='Sol')
        
        # Objet en chute
        ball, = ax1.plot([], [], 'ro', markersize=10, label='Objet')
        trajectory, = ax1.plot([], [], 'b--', alpha=0.5, label='Trajectoire')
        
        # Texte d'information
        info_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, 
                           verticalalignment='top', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax1.legend()
        
        # Graphique 2: Données en temps réel
        ax2.set_xlim(0, max(t_data))
        ax2.set_ylim(min(min(y_data), min(vy_data)), max(max(y_data), max(vy_data)))
        ax2.set_xlabel('Temps (s)')
        ax2.set_ylabel('Valeur')
        ax2.set_title('📊 Données en Temps Réel')
        ax2.grid(True, alpha=0.3)
        
        pos_line, = ax2.plot([], [], 'b-', label='Position Y (m)')
        vel_line, = ax2.plot([], [], 'r-', label='Vitesse Y (m/s)')
        ax2.legend()
        
        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, anim_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Variables d'animation
        frame_data = {'current': 0}
        
        def animate(frame):
            if frame < len(t_data):
                # Position actuelle
                y_curr = y_data[frame]
                vy_curr = vy_data[frame]
                t_curr = t_data[frame]
                
                # Mise à jour de l'objet
                ball.set_data([0], [y_curr])
                trajectory.set_data([0] * (frame + 1), y_data[:frame + 1])
                
                # Texte d'information
                info_text.set_text(f'Temps: {t_curr:.2f} s\n'
                                  f'Hauteur: {y_curr:.2f} m\n'
                                  f'Vitesse: {vy_curr:.2f} m/s')
                
                # Mise à jour des graphiques en temps réel
                pos_line.set_data(t_data[:frame + 1], y_data[:frame + 1])
                vel_line.set_data(t_data[:frame + 1], vy_data[:frame + 1])
                
                return ball, trajectory, info_text, pos_line, vel_line
            
            return ball, trajectory, info_text, pos_line, vel_line
        
        # Lancement de l'animation
        anim = FuncAnimation(fig, animate, frames=len(t_data), 
                           interval=50, blit=False, repeat=True)
        
        plt.tight_layout()
        canvas.draw()
    
    def show_graphs(self):
        """Affiche les graphiques comparatifs"""
        if not self.results:
            messagebox.showwarning("Attention", "Veuillez d'abord lancer la simulation!")
            return
            
        # Création de la fenêtre de graphiques
        graph_window = tk.Toplevel(self.root)
        graph_window.title("📊 Graphiques Comparatifs")
        graph_window.geometry("1200x800")
        
        # Configuration matplotlib
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Couleurs et labels
        colors = {'euler': 'red', 'heun': 'blue', 'rk4': 'green', 'analytical': 'black'}
        labels = {'euler': 'Euler', 'heun': 'Heun', 'rk4': 'Runge-Kutta 4', 'analytical': 'Analytique'}
        
        # 1. Position vs Temps
        for method in ['euler', 'heun', 'rk4', 'analytical']:
            ax1.plot(self.results[method]['t'], self.results[method]['y'], 
                    color=colors[method], label=labels[method], 
                    linewidth=2 if method == 'analytical' else 1)
        ax1.set_xlabel('Temps (s)')
        ax1.set_ylabel('Position Y (m)')
        ax1.set_title('Position Y vs Temps')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Vitesse vs Temps
        for method in ['euler', 'heun', 'rk4', 'analytical']:
            ax2.plot(self.results[method]['t'], self.results[method]['vy'], 
                    color=colors[method], label=labels[method],
                    linewidth=2 if method == 'analytical' else 1)
        ax2.set_xlabel('Temps (s)')
        ax2.set_ylabel('Vitesse Y (m/s)')
        ax2.set_title('Vitesse Y vs Temps')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Erreur absolue
        t_ref = self.results['analytical']['t']
        y_ref = self.results['analytical']['y']
        
        for method in ['euler', 'heun', 'rk4']:
            t_method = self.results[method]['t']
            y_method = self.results[method]['y']
            
            # Interpolation pour comparer aux mêmes points temporels
            min_len = min(len(t_ref), len(t_method))
            if min_len > 1:
                error = np.abs(y_method[:min_len] - y_ref[:min_len])
                ax3.plot(t_ref[:min_len], error, 
                        color=colors[method], label=labels[method])
        
        ax3.set_xlabel('Temps (s)')
        ax3.set_ylabel('Erreur absolue (m)')
        ax3.set_title('Erreur par rapport à la solution analytique')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_yscale('log')
        
        # 4. Comparaison des temps de chute
        methods = ['euler', 'heun', 'rk4']
        times = [self.results[method]['t'][-1] for method in methods]
        analytical_time = self.results['analytical']['t'][-1]
        
        bars = ax4.bar(methods, times, color=[colors[m] for m in methods], alpha=0.7)
        ax4.axhline(y=analytical_time, color='black', linestyle='--', 
                   label=f'Analytique: {analytical_time:.4f} s')
        ax4.set_ylabel('Temps de chute (s)')
        ax4.set_title('Comparaison des temps de chute')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Ajout des valeurs sur les barres
        for bar, time in zip(bars, times):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{time:.4f}s', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, graph_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
    
    def show_analysis(self):
        """Affiche l'analyse automatique des résultats"""
        if not self.results:
            messagebox.showwarning("Attention", "Veuillez d'abord lancer la simulation!")
            return
            
        self.log_result("")
        self.log_result("🔍 ANALYSE AUTOMATIQUE DES RÉSULTATS")
        self.log_result("=" * 60)
        
        # Calcul des erreurs finales
        t_ref = self.results['analytical']['t'][-1]
        errors = {}
        
        for method in ['euler', 'heun', 'rk4']:
            t_method = self.results[method]['t'][-1]
            errors[method] = abs(t_method - t_ref)
        
        # Classement par précision
        sorted_methods = sorted(errors.items(), key=lambda x: x[1])
        
        self.log_result("📊 CLASSEMENT PAR PRÉCISION:")
        for i, (method, error) in enumerate(sorted_methods, 1):
            self.log_result(f"{i}. {method.upper()}: erreur = {error:.6f} s")
        
        # Détermination de la méthode la plus précise
        best_method = sorted_methods[0][0]
        
        self.log_result("")
        self.log_result("🏆 CONCLUSION:")
        self.log_result(f"La méthode la plus précise est: {best_method.upper()}")
        self.log_result("")
        
        # Explication détaillée
        explanations = {
            'euler': """
📝 MÉTHODE D'EULER:
- Méthode la plus simple mais la moins précise
- Approximation linéaire des dérivées
- Erreur d'ordre O(h) où h est le pas de temps
- Accumulation importante d'erreurs sur de longues simulations""",
            
            'heun': """
📝 MÉTHODE DE HEUN:
- Amélioration de la méthode d'Euler
- Utilise une correction basée sur la moyenne de deux estimations
- Erreur d'ordre O(h²) - meilleure que Euler
- Bon compromis entre simplicité et précision""",
            
            'rk4': """
📝 MÉTHODE RUNGE-KUTTA 4:
- Méthode de référence pour la résolution numérique d'EDO
- Utilise 4 estimations pour une approximation très précise
- Erreur d'ordre O(h⁴) - excellente précision
- Plus complexe mais nettement plus précise"""
        }
        
        for method in ['euler', 'heun', 'rk4']:
            self.log_result(explanations[method])
        
        self.log_result("")
        self.log_result("🎯 POURQUOI RUNGE-KUTTA 4 EST GÉNÉRALEMENT LE MEILLEUR:")
        self.log_result("• Approximation d'ordre 4 des dérivées")
        self.log_result("• Erreur qui diminue très rapidement quand le pas diminue")
        self.log_result("• Excellent équilibre entre précision et coût de calcul")
        self.log_result("• Largement utilisé dans la simulation numérique")
        
        if best_method == 'rk4':
            self.log_result("✅ Résultat conforme aux attentes théoriques!")
        else:
            self.log_result("⚠️  Résultat inattendu - vérifiez les paramètres!")
        
        self.log_result("")
        self.log_result("💡 RECOMMANDATIONS:")
        self.log_result("• Pour la précision: utilisez RK4")
        self.log_result("• Pour la rapidité: utilisez Euler avec un pas très petit")
        self.log_result("• Pour un compromis: utilisez Heun")
        self.log_result("• Réduisez le pas de temps pour améliorer la précision")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

# Lancement de l'application
if __name__ == "__main__":
    app = FreeFallSimulator()
    app.run()