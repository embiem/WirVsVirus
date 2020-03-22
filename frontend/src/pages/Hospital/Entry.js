import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import AssignmentIndIcon from '@material-ui/icons/AssignmentInd';
import WorkIcon from '@material-ui/icons/Work';
import CalendarTodayIcon from '@material-ui/icons/CalendarToday';

import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelActions from '@material-ui/core/ExpansionPanelActions';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightBold,
  },
  id: {
    fontSize: theme.typography.pxToRem(12),
    marginLeft: 'auto',
  },
}));

export default function SearchEntry({
  id, title, skills, children,
}) {
  const classes = useStyles();

  return (
    <ExpansionPanel>
      <ExpansionPanelSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1a-content"
        id="panel1a-header"
      >
        <Typography className={classes.heading}>{title}</Typography>
        <Typography className={classes.id}>ID ${id}</Typography>
      </ExpansionPanelSummary>
      <ExpansionPanelDetails>
        <List>
          <ListItem>
            <ListItemAvatar>
              <Avatar>
                <AssignmentIndIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText primary="1. Staatsexamen" secondary="Abschluss" />
          </ListItem>
          <ListItem>
            <ListItemAvatar>
              <Avatar>
                <CalendarTodayIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText primary="24.03. bis 25.04" secondary="Verfuegbarer Zeitraum" />
          </ListItem>
          <ListItem>
            <ListItemAvatar>
              <Avatar>
                <WorkIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={skills
                .reduce((skillsTxt, skill) => `${skillsTxt}, ${skill.name}`, '')
                .substr(1)}
              secondary="Skills"
            />
          </ListItem>
        </List>
      </ExpansionPanelDetails>
      <ExpansionPanelActions>{children}</ExpansionPanelActions>
    </ExpansionPanel>
  );
}
