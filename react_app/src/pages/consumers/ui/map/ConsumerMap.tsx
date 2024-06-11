import {FC, useState} from "react";
import {YMapLocationRequest} from "ymaps3";

import {Box} from "@mui/material";

import {YMap} from "@src/widgets/YMap";
import {coordinates} from "@src/widgets/YMap/const/coordinates";

import {ClusterLayer} from './ClusterLayer';
import {TransformConsumers} from "../../api/getConsumers";

interface ConsumerMapProps {
    data: TransformConsumers[]
}

export const ConsumerMap: FC<ConsumerMapProps> = ({data}) => {
    const [location, setLocation] = useState<YMapLocationRequest>({center: coordinates.districts.VAO, zoom: 11})

    return (
        <Box sx={{height: '700px', width: '100%', position: 'relative', mt: '16px'}}>
            <YMap
                location={location}
                setLocation={setLocation}>
                <ClusterLayer
                    data={data}
                    location={location}
                    setLocation={setLocation}
                />
            </YMap>
        </Box>
    );
};
