package main

import (
    "fmt"
    "time"
)

func printMessage(msg string) {
    for i := 0; i < 3; i++ {
        fmt.Println(msg)
        time.Sleep(time.Millisecond * 500)
    }
}

func main() {
    go printMessage("Goroutine 1")
    go printMessage("Goroutine 2")
    go printMessage("Goroutine 3")

    time.Sleep(time.Second * 2) // 모든 Goroutine이 실행될 시간을 확보
}
