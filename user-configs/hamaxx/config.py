import os

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

os.system("wmname compiz")

screens = [Screen(top = bar.Bar([
		widget.GroupBox(urgent_alert_method='text'),

		widget.Prompt(),

		widget.WindowName(),
		widget.Volume(),
		widget.Systray(),
		widget.Clock('%Y-%m-%d %a %I:%M %p'),
	], 24)) # our bar is 30px high
]

mod = "mod1"
mod1 = "mod4"

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
	Key([mod], "g", lazy.switchgroup()),

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


# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []
for i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
	groups.append(Group(i))
	keys.append(
		Key([mod], i, lazy.group[i].toscreen())
	)
	keys.append(
		Key([mod, 'shift'], i, lazy.window.togroup(i))
	)

# Two basic layouts.
layouts = [
	layout.MonadTall(border_width=1, border_focus='#4444bb'),
	layout.Stack(border_width=1, border_focus='#4444bb'),
	layout.Max(),
]
