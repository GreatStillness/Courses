import {useState} from 'react'

const Header = ({text}) => <div><h1>{text}</h1></div>

const Button = ({handler, text}) => {
    return (
        <>
            <button onClick={handler}>{text}</button>
        </>
    )
}

const StatisticLine = ({text, value, postfix = ''}) => {
    return (
        <>
            <tr>
                <td>{text}</td>
                <td>{value} {postfix}</td>
            </tr>
        </>
    )
}

const Statistics = ({good, neutral, bad}) => {
    if (good === 0 && neutral === 0 && bad === 0) {
        return (
            <div>
                <Header text='statistics'/>
                No feedback given
            </div>
        )
    } else {
        return (
            <div>
                <Header text='statistics'/>
                <table>
                    <tbody>
                    <StatisticLine text='good' value={good}/>
                    <StatisticLine text='neutral' value={neutral}/>
                    <StatisticLine text='bad' value={bad}/>
                    <StatisticLine text='all' value={good + neutral + bad}/>
                    <StatisticLine text='average' value={(good - bad) / (good + neutral + bad)}/>
                    <StatisticLine text='positive' value={good * 100 / (good + neutral + bad)} postfix='%'/>
                    </tbody>
                </table>
            </div>
        )
    }
}

const App = () => {
    // save clicks of each button to its own state
    const [good, setGood] = useState(0)
    const [neutral, setNeutral] = useState(0)
    const [bad, setBad] = useState(0)

    return (
        <div>
            <Header text='give feedback'/>
            <Button handler={() => setGood(good + 1)} text='good'/>
            <Button handler={() => setNeutral(neutral + 1)} text='neutral'/>
            <Button handler={() => setBad(bad + 1)} text='bad'/>
            <Statistics good={good} neutral={neutral} bad={bad}/>
        </div>
    )
}

export default App