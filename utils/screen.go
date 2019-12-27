package utils

import "github.com/gdamore/tcell"

func pollCloseEvents(screen tcell.Screen, quit chan struct{}) {
	for {
		ev := screen.PollEvent()
		switch ev := ev.(type) {
		case *tcell.EventKey:
			switch ev.Key() {
			case tcell.KeyEscape, tcell.KeyEnter:
				close(quit)
				return
			case tcell.KeyCtrlL:
				screen.Sync()
			}
		case *tcell.EventResize:
			screen.Sync()
		}
	}
}
