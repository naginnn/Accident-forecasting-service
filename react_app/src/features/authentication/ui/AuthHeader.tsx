import {Grid, Typography} from "@mui/material";
import {Link} from "../../../shared/ui/link/ui/Link";

interface IAuthenticationHeader {
    topic: string;
    linkTopic: string;
    href: string;
}

export const AuthHeader = ({topic, linkTopic, href}: IAuthenticationHeader) => {
    return (
        <Grid container justifyContent='space-between' alignItems='center' mb='30px'>
            <Grid item>
                <Typography variant='h4' sx={{fontWeight: 600}}>
                    {topic}
                </Typography>
            </Grid>
            <Grid item>
                <Link href={href}>
                    {linkTopic}
                </Link>
            </Grid>
        </Grid>
    )
}
