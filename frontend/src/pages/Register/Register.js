/* eslint-disable no-nested-ternary */
import {
  Container, Paper, TextField, Button, Grid, Box, FormControl, InputLabel, Select, MenuItem,
} from '@material-ui/core';
import Autocomplete from '@material-ui/lab/Autocomplete';
import React, { useState } from 'react';
import { gql } from 'apollo-boost';
import { useQuery } from '@apollo/react-hooks';
import axios from 'axios';
import styles from './Register.module.scss';
import { useAuth0 } from '../../utils/react-auth0-spa';

const HOSPITALS_QUERY = gql`
  {
  hospitals {
    id
    addressCity
    origFid
    globalid
    name
  }
}
`;


const ClinicForm = ({ hospitalChanged }) => {
  const { data: hospitals } = useQuery(
    HOSPITALS_QUERY,
  );

  return (
        <FormControl
          className={styles.formRow}
          fullWidth
        >
<Autocomplete
      id="hospital-name"
      options={hospitals ? hospitals.hospitals : []}
      autoHighlight
      getOptionLabel={(option) => option.name}
      renderOption={(option) => (
        <React.Fragment>
          {option.name} ({option.addressCity})
        </React.Fragment>
      )}
      onChange={(event, newValue) => {
        hospitalChanged(newValue);
      }}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Für welches Krankenhaus suchst Du Unterstützung?"
          variant="outlined"
          inputProps={{
            ...params.inputProps,
            autoComplete: 'new-password', // disable autocomplete and autofill
          }}
        />
      )}
    />


      </FormControl>);
};

const HelperForm = ({
  helperType, helperTypeChanged, helperCapability, helperCapabilityChanged,
}) => <>

    <FormControl
      className={styles.formRow}
      fullWidth
    >


      <FormControl
        className={styles.formRow}
        fullWidth
      >
        <TextField
          id="region"
          label="Meine Postleitzahl"
          name="zipcode"
          placeholder=""
          fullWidth
          margin="normal"
          type="text"
          defaultValue={''}
        />
      </FormControl>

    </FormControl>

    <FormControl
      className={styles.formRow}
      fullWidth
    >
      <InputLabel id="type-select-label">Tätigkeitsbereich</InputLabel>

      <Select
        labelId="type-select-label"
        id="type-select"
        value={helperType}
        onChange={helperTypeChanged}
        name="helperType"
      >
        <MenuItem value={''}>- Bitte wählen -</MenuItem>
        <MenuItem value="admin">Admin</MenuItem>
        <MenuItem value="logistic">Logistik</MenuItem>
        <MenuItem value="medical">Medizin</MenuItem>
      </Select>

    </FormControl>

    <FormControl
      className={styles.formRow}
      fullWidth
    >
      <InputLabel id="type-select-label">Fähigkeiten</InputLabel>

      <Select
        labelId="type-select-label"
        id="type-select"
        value={helperCapability}
        onChange={helperCapabilityChanged}
        name="capability"
      >
        <MenuItem value={''}>- Bitte wählen -</MenuItem>
        <MenuItem value="hotline">Hotline</MenuItem>
        <MenuItem value="testing">Befunde</MenuItem>

        <MenuItem value="care_normal">einfacher Pflegedienst</MenuItem>
        <MenuItem value="care_intensive">erweiterter Pflegedienst</MenuItem>

        <MenuItem value="care_intensive_medical">erweiterter medizinischer Dienst</MenuItem>
        <MenuItem value="care_intensive_medical_ventilation">erweiterter medizinischer Dienst mit Beatmung</MenuItem>

        <MenuItem value="medical_specialist">Medizinischer Spezialist (Arzt)</MenuItem>


      </Select>

    </FormControl>

    </>;

const RegisterPage = () => {
  const [registerType, setRegisterType] = useState('');
  const [helperType, setHelperType] = useState('');
  const [helperCap, setHelperCap] = useState('');
  const [hospital, setHospital] = useState({});

  const { user } = useAuth0();

  const handleTypeSelectChange = (event) => {
    setRegisterType(event.target.value);
  };

  const helperTypeChanged = (event) => {
    setHelperType(event.target.value);
  };

  const helperCapabilityChanged = (event) => {
    setHelperCap(event.target.value);
  };

  const submitForm = async (event) => {
    event.preventDefault();


    const { elements } = event.target;
    const submission = {
      email: elements.email.value,
      profile_type: elements.type.value,
    };

    if (submission.profile_type === 'hospital') {
      submission.hospital = hospital;
    } else {
      submission.helperType = elements.helperType.value;
      submission.capability = elements.capability.value;
    }

    // todo: this should be a custom hook.
    const Axios = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
      headers: {
        Authorization: document.auth_token ? `Bearer ${document.auth_token}` : '',
      },
    });

    const res = await Axios.post('/profile', submission);
    // if (res) redirect to dashboard

    console.log('submitted', res);
  };

  return (
    <div className="py center-vertical">
      <Container>
        <Paper className="paper--content-wrapper">
          <form noValidate autoComplete="off" onSubmit={submitForm}>
            <h1>Registrierung</h1>

            <Grid container spacing={3}>
              <Grid item xs={12}>
                <FormControl
                  className={styles.formRow}
                  fullWidth
                >
                  <InputLabel id="type-select-label">Ich bin...</InputLabel>
                  <Select
                    labelId="type-select-label"
                    id="type-select"
                    name="type"
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
              {
                registerType !== '' ? (
                  registerType === 'helper' ? <HelperForm
                    helperType={helperType}
                    helperCapability={helperCap}
                    helperTypeChanged={helperTypeChanged}
                    helperCapabilityChanged={helperCapabilityChanged}
                  /> : <ClinicForm
                    hospitalChanged={setHospital}
                  />
                ) : ''
              }
              </Grid>
            <Grid item xs={12}>
                {/* E-Mail-Adresse */}
                <FormControl
                  className={styles.formRow}
                  fullWidth
                >
                  <TextField
                    id="mail"
                    label="E-Mailadresse"
                    name="email"
                    placeholder="max.mustermann@gmail.com"
                    fullWidth
                    margin="normal"
                    type="email"
                    defaultValue={user.email}
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
