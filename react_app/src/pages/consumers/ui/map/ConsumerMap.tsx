import {FC, useState} from "react";
import {YMapLocationRequest} from "ymaps3";

import {Box, Button, Paper} from "@mui/material";

import {YMap, YMapControl, YMapControls} from "@src/widgets/YMap";
import {coordinates} from "@src/widgets/YMap/const/coordinates";
import {DownloadExcelButton} from "@src/shared/ui/downloadExlsBtn";
import {ErrorWrapper} from "@src/entities/errorWrapper";

import {ClusterLayer} from './ClusterLayer';
import {TransformConsumers} from "../../api/getConsumers";
import {useDownloadConsumers} from "../../api/downloadExcel";

interface ConsumerMapProps {
    data: TransformConsumers[]
}

export const ConsumerMap: FC<ConsumerMapProps> = ({data}) => {
    const [location, setLocation] = useState<YMapLocationRequest>({center: coordinates.districts.VAO, zoom: 9})
    const {downloadExcel, error} = useDownloadConsumers()

    return (
        <ErrorWrapper
            snackBarErrors={{
                errors: [{error, message: 'Не удалось загрузить excel'}]
            }}
        >
            <Box sx={{height: '700px', width: '100%', position: 'relative', mt: '16px'}}>
                <YMap
                    location={location}
                    setLocation={setLocation}>
                    <YMapControls position="top right">
                        <YMapControl>
                            <DownloadExcelButton
                                sx={{width: '190px'}}
                                onClick={downloadExcel}
                            >
                                Загрузить Excel
                            </DownloadExcelButton>
                        </YMapControl>
                    </YMapControls>
                    <ClusterLayer
                        data={data}
                        location={location}
                        setLocation={setLocation}
                    />
                </YMap>
            </Box>
        </ErrorWrapper>
    );
};
