import {
  AppBar,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Toolbar,
  Typography,
  ListItemIcon,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { Inbox as InboxIcon, Mail as MailIcon, Menu } from '@material-ui/icons';
import clsx from 'clsx';
import React, { useState } from 'react';
import { Link as RouterLink } from '@reach/router';
import styles from './Header.module.scss';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

const Header = () => {
  const classes = useStyles();
  const [offcanvasOpen, setOffcanvasOpen] = useState(false);

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setOffcanvasOpen(open);
  };

  const list = () => (
    <div
      className={clsx(classes.list)}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        {[
          { url: '/profile', title: 'Login' },
          { url: '/register', title: 'Registrieren' },
          { url: '/hospital', title: 'Kliniken-Dashboard' },
          { url: '/profile', title: 'Helfer:Innen-Dashboard' },
          { url: '/hospital/create-invitation', title: 'Ausschreibung erstellen' },
        ].map((item) => (
          <RouterLink to={item.url} key={item.title} className={styles.offcanvasLink}>
            <ListItem button>
              <ListItemText primary={item.title} />
            </ListItem>
          </RouterLink>
        ))}
      </List>
      <Divider />
      {/* DUMMY STUFF */}
      {/* <List>
        {['All mail', 'Trash', 'Spam'].map((text, index) => (
          <ListItem button key={text}>
            <ListItemIcon>{index % 2 === 0 ? <InboxIcon /> : <MailIcon />}</ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List> */}
    </div>
  );

  return (
    <>
      <AppBar position="fixed" className={styles.header}>
        <Toolbar>
          <IconButton
            edge="start"
            className={classes.menuButton}
            color="inherit"
            aria-label="menu"
            onClick={toggleDrawer(true)}
            onKeyDown={toggleDrawer(true)}
          >
            <Menu />
          </IconButton>
          <Typography variant="h6" className={classes.title}>
            WE MATCH 4 health
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer open={offcanvasOpen} onClose={toggleDrawer(false)}>
        {list()}
      </Drawer>
    </>
  );
};

export default Header;
