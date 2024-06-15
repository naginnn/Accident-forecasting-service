import {FC} from "react";

import {Box, Breadcrumbs, Divider, Grid} from "@mui/material";

import {withMenu} from "@src/widgets/menuWrapper";
import {Link} from "@src/shared/ui/link";
import {PageWrapper} from "@src/entities/pageWrapper";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {Events} from "./Events";

export const Settings: FC = withMenu(() => {
    return (
        <Box sx={{overflow: 'hidden'}}>
            <Breadcrumbs>
                <Link sx={{color: 'black'}}>
                    Настройки
                </Link>
            </Breadcrumbs>
            <PageWrapper>
                <PaperWrapper>
                    <Grid container>
                        <Grid item xs={6}>
                            <Events/>
                        </Grid>
                        <Divider orientation="vertical" variant="middle" flexItem/>
                    </Grid>
                </PaperWrapper>
            </PageWrapper>
        </Box>
    );
}, 'Настройки')
