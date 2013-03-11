import os

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

os.system("wmname compiz")

screens = [Screen(top = bar.Bar([
		widget.GroupBox(urgent_alert_method='text', padding=1, borderwidth=1),

		widget.Prompt(),
		widget.Notify(),

		widget.WindowName(fontsize=14, padding=10, foreground='dddddd'),

		widget.Battery(fontsize=14, foreground='dddddd'),
		widget.Systray(),
		widget.Clock('%Y-%m-%d %a %I:%M %p', fontsize=14, foreground='dddddd'),
	], 20))
]

dmenu = 'dmenu_run -i -b -p ">>>" -fn "Ariel" -nb "#000" -nf "#fff" -sb "#15181a" -sf "#fff"'

mod = "mod1"
mod1 = "mod4"

def cmd_renamegroup(manager):
	def f(name):
		del manager.groupMap[manager.currentGroup.name]
		manager.currentGroup.name = name
		manager.groupMap[name] = manager.currentGroup

	prompt = manager.widgetMap.get('prompt')
	prompt.startInput('name: ', f, "group", strict_completer=True)

keys = [
	Key([mod], "space", lazy.nextlayout()),
	Key([mod, 'shift'], "c", lazy.window.kill()),

	Key([mod], "k", lazy.layout.down()),
	Key([mod], "j", lazy.layout.up()),

	Key([mod], "l", lazy.layout.previous()),
	Key([mod], "h", lazy.layout.next()),

	Key([mod, 'shift'], "k", lazy.layout.grow()),
	Key([mod, 'shift'], "j", lazy.layout.shrink()),

	Key([mod], "n", lazy.layout.normalize()),
	Key([mod], "o", lazy.layout.maximize()),

	Key([mod], "Tab", lazy.layout.down()),

	Key([mod], "Return", lazy.layout.shuffle_down()),
	Key([mod, "shift"], "space", lazy.layout.toggle_split()),
	#Key([mod, "shift"], "j", lazy.layout.shuffle_up()),

    Key([mod], "w", lazy.to_screen(0)),
    Key([mod], "e", lazy.to_screen(1)),

	Key([mod], "t", lazy.window.disable_floating()),

	# interact with prompts
	Key([mod], "r", lazy.spawncmd()),
	Key([mod], 'f', lazy.spawn(dmenu)),

	Key([mod],  "g", lazy.switchgroup()),
	Key([mod, "shift"], "g", lazy.function(cmd_renamegroup)),

	# start specific apps
	Key([mod, 'shift'], "Return", lazy.spawn("gnome-terminal")),

	Key([mod, "shift"], "r", lazy.restart()),

	# Change the volume if your keyboard has special volume keys.
	Key(
		[], "XF86AudioRaiseVolume",
		lazy.spawn("amixer -c 0 -q set Master 2dB+")
	),
	Key(
		[], "XF86AudioLowerVolume",
		lazy.spawn("amixer -c 0 -q set Master 2dB-")
	),
	Key(
		[], "XF86AudioMute",
		lazy.spawn("amixer -c 0 -q set Master toggle")
	),

	Key([mod, 'control'], 'l', lazy.spawn('/usr/bin/gnome-screensaver-command -l')),
	Key([mod, 'control'], 'q', lazy.spawn('/usr/bin/gnome-session-quit --logout --no-prompt')),
	Key([mod, 'shift', 'control'], 'q', lazy.spawn('/usr/bin/gnome-session-quit --power-off')),
]

# This allows you to drag windows around with the mouse if you want.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(),
		start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(),
		start=lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.bring_to_front())
	# TODO always front
]

floating_layout = layout.Floating(
		border_width=0
		,max_border_width=0
		,fullscreen_border_width=0
)
@hook.subscribe.client_new
def floats(window):
	if(window.window.get_wm_type() == "dialog" or window.window.get_wm_transient_for()):
		window.floating = True
	if (window.name == 'Desktop'):
		window.minimized = True

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []
for kbs, name in (("quoteleft", "home"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),):
	groups.append(Group(name))
	keys.append(
		Key([mod], kbs, lazy.group[name].toscreen())
	)
	keys.append(
		Key([mod, 'shift'], kbs, lazy.window.togroup(name))
	)

# Two basic layouts.
layouts = [
	layout.MonadTall(border_width=1, border_focus='#4444bb'),
	layout.Max(),
]
