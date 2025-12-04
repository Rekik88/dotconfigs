# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

import libqtile.resources
from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

mod = "mod4"
terminal = guess_terminal()
fileManager = "thunar"
browser = "zen-browser"


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "e", lazy.spawn(fileManager), desc="Launch file manager"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key(
        [mod],
        "p",
        lazy.spawn("sh -c ~/.config/rofi/scripts/power"),
        desc="Launch power menu",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

lay_config = {
    "margin": 1,
    "font": "CaskaydiaCove Nerd Font",
    "border_width": 2,
    "border_normal": "#414868",
    "border_focus": "#a9b1d6",
    "border_on_single": True,
}

layouts = [
    layout.Columns(**lay_config),
    layout.Max(**lay_config),
    # layout.Floating(**lay_config),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="CaskaydiaMono Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")

powerline = {
    "decorations": [PowerLineDecoration(stroke_weight=1, stroke_colour="#414868")]
}


def power():
    qtile.spawn("sh -c ~/.config/rofi/scripts/power")


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=5, background="#15161e"),
                widget.Image(
                    filename="~/.config/qtile/Assets/launch_Icon.svg",
                    margin=2,
                    background="#15161e",
                    mouse_callbacks={"Button1": power},
                    **powerline,
                ),
                widget.GroupBox(
                    visible_groups=["1", "2", "3", "4"],
                    borderwidth=3,
                    highlight_method="block",
                    active="#c0caf5",
                    inactive="#414868",
                    block_highlight_text_color="#15161e",
                    background="#1a1b26",
                    this_current_screen_border="#a9b1d6",
                    urgent_border="#f7768e",
                    disable_drag=True,
                    **powerline,
                ),
                widget.CurrentLayout(
                    background="#15161e",
                    **powerline,
                ),
                widget.Spacer(),
                widget.WindowName(
                    background="#15161e",
                    empty_group_string="Desktop",
                    foreground="#c0caf5",
                    width=bar.CALCULATED,
                ),
                widget.Spacer(**powerline),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(
                    background="#1a1b26",
                ),
                widget.Volume(
                    background="#1a1b26",
                    foreground="#c0caf5",
                    #   mute_command="pamixer --toggle-mute",
                    #   volume_up_command="pamixer -i 5",
                    #   volume_down_command="pamixer -d 5",
                    #   get_volume_command="pamixer --get-volume-human",
                    #   update_interval=0.2,
                    #   emoji=True,
                    theme_path="~/.config/qtile/Assets/volume",
                ),
                # widget.ALSAWidget(
                #     mode="icon",
                #      theme_path="~/.config/qtile/Assets/volume",
                #        **powerline,
                #     ),
                # widget.Backlight(
                #     background="#1a1b26",
                #  ),
                widget.IWD(
                    show_image=True,
                    show_text=False,
                    background="#1a1b26",
                    active_colour="#c0caf5",
                ),
                # widget.UPowerWidget(),
                widget.BatteryIcon(
                    background="#1a1b26",
                    theme_path="~/.config/qtile/Assets/battery",
                    **powerline,
                ),
                # widget.Battery(
                #    background="#1a1b26",
                #    format="{percent:2.0%}",
                # ),
                widget.Clock(
                    background="#15161e",
                    format="%d/%m/%y %H:%M",
                ),
            ],
            20,
            margin=1,
            border_width=2,  # Draw top and bottom borders
            border_color="#414868",
            background="#15161e",
        ),
        background="#000000",
        wallpaper=logo,
        wallpaper_mode="center",
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    **lay_config,
)


@hook.subscribe.startup_once
def startup_once():
    subprocess.run([os.path.expanduser("~/.config/qtile/autostart.sh")])


auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
