import {
  Container, Paper, TextField, Button, Grid, Box, FormControl, InputLabel, Select, MenuItem,
} from '@material-ui/core';
import React, { useState } from 'react';
import styles from './Register.module.scss';

const RegisterPage = () => {
  const [registerType, setRegisterType] = useState('');

  const handleTypeSelectChange = (event) => {
    setRegisterType(event.target.value);
  };

  const submitForm = (event) => {
    event.preventDefault();
    console.log('Form is submitted');
  };

  return (
    <div className="py center-vertical">
      <Container>
        <Paper className="paper--content-wrapper">
          <form noValidate autoComplete="off" onSubmit={submitForm}>
            <h1>Registrierung</h1>

            <Grid container spacing={3}>
              <Grid item xs={12}>
                {/* Krankenhausname */}
                <FormControl
                  className={styles.formRow}
                  fullWidth
                >
                  <InputLabel id="type-select-label">Ich bin...</InputLabel>
                  <Select
                    labelId="type-select-label"
                    id="type-select"
                    value={registerType}
                    onChange={handleTypeSelectChange}
                  >
                    <MenuItem value={''}>- Bitte wählen -</MenuItem>
                    <MenuItem value="helper">HelferIn</MenuItem>
                    <MenuItem value="hospital">Krankenhaus</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                {/* Krankenhausname */}
                <FormControl
                  className={styles.formRow}
                  fullWidth
                >
                  <TextField
                    id="hospital-name"
                    label="Name"
                    placeholder="Name des Krankenhauses"
                    fullWidth
                    margin="normal"
                  />
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                {/* E-Mail-Adresse */}
                <FormControl
                  className={styles.formRow}
                  fullWidth
                >
                  <TextField
                    id="mail"
                    label="E-Mailadresse"
                    placeholder="max.mustermann@gmail.com"
                    fullWidth
                    margin="normal"
                    type="email"
                  />
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                {/* E-Mail-Adresse bestätigen */}
                <FormControl
                  className={styles.formRow}
                  fullWidth
                >
                  <TextField
                    id="mail-confirm"
                    label="E-Mailadresse wiederholen"
                    placeholder="max.mustermann@gmail.com"
                    fullWidth
                    margin="normal"
                    type="email"
                  />
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                {/* Passwor`t */}
                <FormControl
                  className={styles.formRow}
                  fullWidth
                >
                  <TextField
                    id="password"
                    label="Passwort"
                    placeholder="Passwort"
                    fullWidth
                    margin="normal"
                    type="password"
                  />
                </FormControl>
              </Grid>

              {/* Submit */}
              <Grid item xs={12}>
                <Box className={styles.formRow}>
                  {/* Abort */}
                  <Button variant="contained">Abbrechen</Button>

                  {/* Submit */}
                  <Button
                    variant="contained"
                    color="primary"
                    className="float-right"
                    type="submit"
                  >
                    Registrieren
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </form>
        </Paper>
      </Container>
    </div>
  );
};

export default RegisterPage;
