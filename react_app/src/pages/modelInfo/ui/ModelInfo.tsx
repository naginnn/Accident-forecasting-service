//@ts-nocheck
import {FC, useMemo} from "react";
import {Box, Breadcrumbs, Typography} from "@mui/material";

import {withMenu} from "@src/widgets/menuWrapper";
import {Link} from "@src/shared/ui/link";
import {PageWrapper} from "@src/entities/pageWrapper";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {TableFilter} from "@src/widgets/tableFilter";

import {useGetModelInfoQuery} from "../api/modelInfo";
import {featureImportanceRuVal} from "../const/featureImportanceRuVal";

export const ModelInfo: FC = withMenu(() => {
    const {data, error, isLoading} = useGetModelInfoQuery()

    const renamedData = useMemo(() => {
        if (data?.feature_importance?.feature_importances?.length) {
            return data?.feature_importance.feature_importances
                .map(info => {
                    return {
                        ...info,
                        name: featureImportanceRuVal[info.name as unknown as keyof typeof featureImportanceRuVal]
                    }
                })
        }
    }, [data])

    return (
        <LoadingWrapper isLoading={isLoading} displayType='normal'>
            <ErrorWrapper
                fullSizeError={{error, blockContent: true}}
            >
                <Box sx={{overflow: 'hidden'}}>
                    <Breadcrumbs>
                        <Link sx={{color: 'black'}}>
                            Информация о модели
                        </Link>
                    </Breadcrumbs>
                    <PageWrapper>
                        <PaperWrapper>
                            <Typography variant='h5' gutterBottom>
                                Важные признаки
                            </Typography>
                            {
                                renamedData?.length
                                ? <TableFilter
                                        data={renamedData}
                                        withPagination
                                    >
                                        <TableFilter.Banner withSearch/>
                                        <TableFilter.Cell keyName='name' id='name' topic='Название'/>
                                        <TableFilter.SortCell keyName='score' id='score' topic='Вес'/>
                                    </TableFilter>
                                    : <Typography>Данные отсутствуют</Typography>
                            }
                        </PaperWrapper>
                    </PageWrapper>
                </Box>
            </ErrorWrapper>
        </LoadingWrapper>

    );
}, 'Информация о модели')