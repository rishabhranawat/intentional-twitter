// @useClient
import React, { useState } from 'react'

function FormBox() {
    const [inputValue, setInputValue] = useState('');
    const [response, setResponse] = useState('');

    const fetchData = async () => {
        try {
            const response = await fetch("");
            const data = await response.json();
            setResponse(`Response: ${data.title}`);
        } catch (error) {
            console.log('Error fetching data:', error)
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await fetchData();
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label htmlFor="inputField">Research Paper: </label>
                <input
                    type="text"
                    id="inputField"
                    name="inputField"
                    placeholder="Insert url here"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                />

                <button type="submit">Submit</button>
            </form>
            <div>
                {response && <p>{response}</p>}
            </div>
        </div>
    );
}

export default FormBox