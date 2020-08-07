import React, { Component } from './node_modules/react';

class Counter extends Component {
    state = {
        count: 0
    }

    render() {
        return (
            <div>
                <span>{this.fotmatCount()}</span>
                <button>Increment</button>
            </div>
        )
    }

    formatCount() {
        const { count } = this.state
        return count === 0 ? 'Zero' : count
    }
}

export default Counter;