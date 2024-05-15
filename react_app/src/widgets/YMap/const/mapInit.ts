import ReactDOM from "react-dom";
import React from "react";

const ymaps3Reactify = await ymaps3.import('@yandex/ymaps3-reactify');
const reactify = ymaps3Reactify.reactify.bindTo(React, ReactDOM);

export const {YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapScaleControl, YMapControls, LngLat} = reactify.module(ymaps3);