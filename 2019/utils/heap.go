package utils

// Node is a node in the priority queue
type Node struct {
	value    interface{}
	distance int
	index    int
}

// PriorityQueue implemented using the heap interface
// From https://golang.org/pkg/container/heap/
type PriorityQueue []*Node

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].distance < pq[j].distance
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

// Push implements heap.Interface's Push
func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Node)
	item.index = n
	*pq = append(*pq, item)
}

// Pop implements heap.Interface's Pop
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// NewNode constructs a node instance
func NewNode(value interface{}, distance int) Node {
	return Node{value, distance, 0}
}

// GetValue returns the value of the node
func (i *Node) GetValue() interface{} {
	return i.value
}

// GetDistance returns the distance of the node from the source
func (i *Node) GetDistance() int {
	return i.distance
}

// SetDistance updates the distance of a node
func (i *Node) SetDistance(dist int) {
	i.distance = dist
}

// GetIndex returns the index of the node in the heap
func (i *Node) GetIndex() int {
	return i.index
}
