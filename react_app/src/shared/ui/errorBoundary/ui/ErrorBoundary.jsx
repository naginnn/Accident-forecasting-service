export class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError() {
        return { hasError: true };
    }

    render() {
        if (this.state.hasError && this.props.fallback) {
            return this.props.fallback;
        } else if (this.props.fallback) {
            <div>Error happens</div>
        }

        return this.props.children;
    }
}