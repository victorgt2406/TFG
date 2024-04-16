import React, { useState } from 'react';

const ReactComponent = () => {
    const [count, setCount] = useState(0);

    return (
        <div>
            <h3>Count: {count}</h3>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
};

export default ReactComponent;
