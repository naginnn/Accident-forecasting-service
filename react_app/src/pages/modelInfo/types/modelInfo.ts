export type FeatureImportance = {
    name: string
    score: number
}

export type ModelInfo = {
    id: number
    name: string
    metrics: string
    path: string
    accuracy: number
    feature_importance: {
        feature_importances: FeatureImportance[]
    }
}