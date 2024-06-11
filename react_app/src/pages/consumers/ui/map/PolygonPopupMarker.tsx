import {FC} from "react";
import {LngLat} from "ymaps3";

import CloseIcon from '@mui/icons-material/Close';

import {YMapFeature, YMapMarker} from "@src/widgets/YMap";
import {useToggle} from "@src/shared/hooks/useToggle";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";
import {IconButton} from "@mui/material";
import {orange, red } from "@mui/material/colors";

interface PolygonPopupMarkerProps {
    id: string
    isWarning: boolean
    isApproved: boolean
    center: LngLat
    polygon: LngLat[]
}

export const PolygonPopupMarker: FC<PolygonPopupMarkerProps> = ({id, isWarning, isApproved, center, polygon}) => {
    const {on: openPopup, off: closePopup, value: isOpenPopup} = useToggle()

    return (
        <>
            <YMapMarker key={id} coordinates={center} source="clusterer-source">
                <YMapFeature
                    onClick={openPopup}
                    geometry={{
                        type: 'Polygon',
                        coordinates: [polygon]
                    }}
                    style={{
                        cursor: 'pointer',
                        stroke: [{
                            color: isApproved ? red[500] : isWarning ?  orange[500] : '#006efc',
                            width: 2
                        }],
                        fill: isApproved ? red[100] : isWarning ?  orange[100] : 'rgba(56, 56, 219, 0.5)'
                    }}
                />
            </YMapMarker>
            {
                isOpenPopup &&
                <YMapMarker
                    coordinates={center}
                    zIndex={1000}
                    blockBehaviors
                >
                    <PaperWrapper sx={{maxHeight: '500px', position: 'relative', minWidth: '300px'}}>
                        <IconButton
                            sx={{ml: 'auto', display: 'block'}}
                            onClick={closePopup}
                        >
                            <CloseIcon/>
                        </IconButton>
                        {
                            center.toString()
                        }
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit ipsum nihil, odio repellat sed
                        voluptate. Aliquid aperiam, blanditiis delectus dolor eligendi, iste laborum quia rem rerum
                        tempora, unde vitae voluptatibus!
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit ipsum nihil, odio repellat sed
                        voluptate. Aliquid aperiam, blanditiis delectus dolor eligendi, iste laborum quia rem rerum
                        tempora, unde vitae voluptatibus!
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit ipsum nihil, odio repellat sed
                        voluptate. Aliquid aperiam, blanditiis delectus dolor eligendi, iste laborum quia rem rerum
                        tempora, unde vitae voluptatibus!
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit ipsum nihil, odio repellat sed
                        voluptate. Aliquid aperiam, blanditiis delectus dolor eligendi, iste laborum quia rem rerum
                        tempora, unde vitae voluptatibus!
                    </PaperWrapper>
                </YMapMarker>
            }
        </>
    );
};
