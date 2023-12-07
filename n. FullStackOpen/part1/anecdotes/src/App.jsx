import {useState} from 'react'

const Header = ({text}) => <div><h1>{text}</h1></div>

const Anecdote = ({anecdotes, points, anecdoteIndex}) => {
    return (
        <div>
            {anecdotes[anecdoteIndex]}
            <br/>
            has {points[anecdoteIndex]} votes
        </div>
    )
}
const TopAnecdote = ({anecdotes, points}) => {
    let max = 0
    let maxIndex = 0
    for (let i = 0; i < points.length; i++) {
        if (points[i] > max) {
            max = points[i]
            maxIndex = i
        }
    }
    return (
        <div>
            <Anecdote anecdotes={anecdotes} points={points} anecdoteIndex={maxIndex}/>
        </div>
    )
}
const App = () => {
    const anecdotes = [
        'If it hurts, do it more often.',
        'Adding manpower to a late software project makes it later!',
        'The first 90 percent of the code accounts for the first 10 percent of the development time...The remaining 10 percent of the code accounts for the other 90 percent of the development time.',
        'Any fool can write code that a computer can understand. Good programmers write code that humans can understand.',
        'Premature optimization is the root of all evil.',
        'Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it.',
        'Programming without an extremely heavy use of console.log is same as if a doctor would refuse to use x-rays or blood tests when diagnosing patients.',
        'The only way to go fast, is to go well.'
    ]
    const [points, setPoints] = useState([0, 0, 0, 0, 0, 0, 0, 0])

    const [selected, setSelected] = useState(0)

    const upvote = () => {
        const newPoints = [...points]
        newPoints[selected] += 1
        setPoints(newPoints)

    }
    const chooseRandomAnecdote = () => {
        const randomIndex = Math.floor(Math.random() * anecdotes.length)
        setSelected(randomIndex)
    }

    return (
        <div>
            <Header text='Anecdote of the day'/>
            <Anecdote anecdotes={anecdotes} points={points} anecdoteIndex={selected}/>
            <button onClick={upvote}>vote</button>
            <button onClick={chooseRandomAnecdote}>next anecdote</button>
            <Header text='Anecdote with most votes'/>
            <TopAnecdote anecdotes={anecdotes} points={points}/>
        </div>
    )
}

export default App