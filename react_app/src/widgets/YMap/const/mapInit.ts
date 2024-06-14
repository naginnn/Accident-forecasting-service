import ReactDOM from "react-dom";
import React from "react";

const [ymaps3Reactify] = await Promise.all([ymaps3.import('@yandex/ymaps3-reactify'), ymaps3.ready]);
const reactify = ymaps3Reactify.reactify.bindTo(React, ReactDOM);
export const {
    YMap,
    YMapDefaultSchemeLayer,
    YMapDefaultFeaturesLayer,
    YMapScaleControl,
    YMapControls,
    YMapControl,
    YMapFeature,
    YMapControlButton,
    YMapLayer,
    YMapMarker,
    YMapFeatureDataSource,
    YMapListener
} = reactify.module(ymaps3);

export const {
    YMapZoomControl
} = reactify.module(await ymaps3.import('@yandex/ymaps3-controls@0.0.1'));

export const {
    YMapClusterer,
    clusterByGrid
} = reactify.module(await ymaps3.import('@yandex/ymaps3-clusterer@0.0.1'))

export const {
    YMapDefaultMarker
} = reactify.module(await ymaps3.import('@yandex/ymaps3-markers@0.0.1'));


