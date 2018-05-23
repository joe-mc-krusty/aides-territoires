import React from "react";
import { reduxForm } from "redux-form";
import SlideDown from "modules/ui-kit/reactSpring/SlideDown";
import CheckboxGroup from "modules/ui-kit/reduxForm/CheckboxGroup";
import { ArrowDown, ArrowUp } from "modules/ui-kit/bulma/Icons";
import enums from "modules/aide/enums";

const styles = {
  searchFilters: {
    background: "rgb(250, 250, 250)"
  },
  filter: {
    marginBottom: "0.5 rem",
    borderBottom: "solid rgb(220, 220, 220) 1px",
    padding: "1rem"
  },
  label: {
    paddingBottom: "0.5 rem",
    cursor: "pointer",
    textTransform: "uppercase"
  }
};

let SearchFilters = class extends React.Component {
  state = {
    activeFilters: {
      perimetreApplication: true,
      type: true,
      etape: false,
      formeDeDiffusion: false,
      destination: false,
      thematiques: false
    }
  };
  handleLabelClick = filterId => {
    const newFilters = {
      ...this.state.activeFilters,
      [filterId]: !this.state.activeFilters[filterId]
    };
    this.setState({
      activeFilters: newFilters
    });
  };
  render() {
    // const { handleSubmit, pristine, reset, submitting } = props;
    return (
      <form style={styles.searchFilters}>
        {/***  PERIMETRE D'APPLICATION ***/}
        {/*
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("perimetreApplicationType")}
          >
            Périmètre d'application
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.perimetreApplication}
          >
            <CheckboxGroup
              name="perimetreApplicationType"
              options={PERIMETRE_APPLICATION_OPTIONS}
            />
          </SlideDown>
        </div>
        */}
        {/*** TYPE D'AIDE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("type")}
          >
            {this.state.activeFilters.type ? <ArrowUp /> : <ArrowDown />}
            Type d'aide{" "}
          </label>
          <SlideDown maxHeight={400} show={this.state.activeFilters.type}>
            <CheckboxGroup name="type" options={enums.type} />
          </SlideDown>
        </div>

        {/*** ETAPE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("etape")}
          >
            {this.state.activeFilters.etape ? <ArrowUp /> : <ArrowDown />}
            Étape
          </label>
          <SlideDown maxHeight={400} show={this.state.activeFilters.etape}>
            <CheckboxGroup name="etape" options={enums.etape} />
          </SlideDown>
        </div>

        {/*** MODALITE DE DIFFUSION ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("formeDeDiffusion")}
          >
            {this.state.activeFilters.formeDeDiffusion ? (
              <ArrowUp />
            ) : (
              <ArrowDown />
            )}
            Modalité de diffusion
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.formeDeDiffusion}
          >
            <CheckboxGroup
              name="formeDeDiffusion"
              options={enums.formeDeDiffusion}
            />
          </SlideDown>
        </div>

        {/*** DESTINATION DE L'AIDE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("destination")}
          >
            {this.state.activeFilters.destination ? <ArrowUp /> : <ArrowDown />}
            Destination
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.destination}
          >
            <CheckboxGroup name="destination" options={enums.destination} />
          </SlideDown>
        </div>

        {/***  THEMATIQUES ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("thematiques")}
          >
            {this.state.activeFilters.thematiques ? <ArrowUp /> : <ArrowDown />}
            Thématiques
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.thematiques}
          >
            <CheckboxGroup name="thematiques" options={enums.thematiques} />
          </SlideDown>
        </div>
      </form>
    );
  }
};

/*
const validate = values => {
  const errors = {};
  if (!values.nom || values.nom.trim().length === 0) {
    errors.nom = "Le champ nom est requis";
  }
  return errors;
};
*/

SearchFilters = reduxForm({
  // a unique name for the form
  form: "searchFilters"
})(SearchFilters);

/*
SearchFilters = connect(state => {
  return {
    formValues: state.form.searchFilters ? state.form.searchFilters.values : {}
  };
})(SearchFilters);
*/

export default SearchFilters;
