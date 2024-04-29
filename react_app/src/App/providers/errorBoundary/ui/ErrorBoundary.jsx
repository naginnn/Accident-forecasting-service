// Обработчик ошибки во время рендера и в хуках
export class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props)

        this.state = {hasError: false}
    }

    static getDerivedStateFromError() {
        return {hasError: true}
    }

    render() {
        if (this.state.hasError) {
            return <div>ERROR BOUNDARY CATCH ERROR</div>
        }

        return this.props.children
    }
}

