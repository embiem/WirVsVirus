import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Modal from '@material-ui/core/Modal';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

function getModalStyle() {
  return {
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
  };
}

const useStyles = makeStyles((theme) => ({
  paper: {
    position: 'absolute',
    width: 800,
    backgroundColor: theme.palette.background.paper,
    border: `2px solid ${theme.palette.primary.light}`,
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
  },
  container: {
    width: '100%',
  },
}));

export default function RequestModal({ open, onSubmit, onClose }) {
  const classes = useStyles();
  // getModalStyle is not a pure function, we roll the style only on the first render
  const [modalStyle] = React.useState(getModalStyle);
  const [infoText, setInfoText] = React.useState('');

  return (
    <Modal
      aria-labelledby="simple-modal-title"
      aria-describedby="simple-modal-description"
      open={open}
      onClose={onClose}
    >
      <div style={modalStyle} className={classes.paper}>
        <Typography variant="h4" gutterBottom>
          Informationen fuer den Helfer
        </Typography>
        <Grid container spacing={2} direction="column" justify="center" alignItems="center">
          <Grid item className={classes.container}>
            <TextField
              value={infoText}
              onChange={(e) => setInfoText(e.target.value)}
              label="Weitere Informationen zur Taetigkeit"
              variant="outlined"
              fullWidth
              multiline
              rows={4}
            />
          </Grid>
          <Grid item>
            <Button
              onClick={() => {
                onSubmit({ infoText });
              }}
              variant="contained"
              color="primary"
            >
              Anfrage abschicken
            </Button>
          </Grid>
        </Grid>
      </div>
    </Modal>
  );
}
