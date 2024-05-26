import {styled} from '@mui/system';
import {Tabs} from '@mui/base/Tabs';
import {TabPanel} from '@mui/base/TabPanel';
import {TabsList} from '@mui/base/TabsList';
import {buttonClasses} from '@mui/base/Button';
import {Tab as BaseTab, tabClasses} from '@mui/base/Tab';
import {TabOwnProps} from "@mui/base/Tab/Tab.types";

export const BookmarksTabs = styled(Tabs)`
  margin-top: 4px;
`

const StyledTab = styled(BaseTab)(
    ({theme}) => `
  background-color: ${theme.palette.grey[100]};
  opacity: 0.9;
  color: ${theme.palette.primary.main};
  cursor: pointer;
  width: fit-content;
  min-width: 150px;
  padding: 4px 12px;
  border: none;
  box-shadow: 0px -2px 3px 0px rgba(0,0,0,0.12);
  border-bottom: none;
  border-radius: 8px 8px 0px 0px;
  display: flex;
  position: relative;
  justify-content: center;
  
  span {
        background-color: rgba(0, 0, 0, 0.12);
        height: 1px;
        z-index: 1;
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
    }

  &:hover {
    background-color: ${theme.palette.grey[200]};
  }

  &.${tabClasses.selected} {
    background-color: #fff;
    color: ${theme.palette.primary.light};
    
    span {
        background-color: ${theme.palette.primary.light};
        height: 2px;
    }
  }

  &.${buttonClasses.disabled} {
    opacity: 0.5;
    cursor: not-allowed;
  }
  `
);

export const BookmarksTabPanel = styled(TabPanel)`
  width: 100%;
`;

export const BookmarksTabsList = styled(TabsList)`
  min-width: 200px;
  display: flex;
  gap: 8px;
  align-items: center;
  align-content: space-between;
`

export const BookmarksTab = ({children, ...props}: TabOwnProps & { children: string }) => {
    return <StyledTab {...props}>
        {children}
    </StyledTab>
}
