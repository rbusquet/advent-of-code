package utils

import "github.com/gdamore/tcell"

// NewScreen returns a new tcell screen, and a channel to wait for esc/enter
func NewScreen() (tcell.Screen, chan struct{}) {
	screen, err := tcell.NewScreen()
	if err != nil {
		panic(err)
	}
	quit := make(chan struct{})

	go func() {
		for {
			ev := screen.PollEvent()
			switch ev := ev.(type) {
			case *tcell.EventKey:
				switch ev.Key() {
				case tcell.KeyEscape, tcell.KeyEnter:
					close(quit)
					return
				}
			case *tcell.EventResize:
				screen.Sync()
			}
		}
	}()
	return screen, quit
}
