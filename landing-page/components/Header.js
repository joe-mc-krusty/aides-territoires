import React from "react";
import getConfig from "next/config";
const { publicRuntimeConfig } = getConfig();
export default class Header extends React.Component {
  render() {
    return (
      <section id="aides-territoires" className="hero ">
        <header className="header ">
          <div className="header-overlay ">
            <div className="hero-body ">
              <div className="container ">
                <h1 className="title ">UN OUTIL POUR LES COLLECTIVITÉS</h1>
                <h2 className="subtitle ">
                  <p>
                    {publicRuntimeConfig.GRAPHQL_URL} Identifiez en quelques
                    clics toutes les aides disponibles sur votre territoire pour
                    vos projets d'aménagements durables.
                    <br />
                    <br /> Un service actuellement expérimenté pour les projets
                    de quartiers durables, dont les EcoQuartiers.
                  </p>
                </h2>
                <div className="button is-large is-primary ">
                  <a
                    className="button-lancez-la-recherche js-scrollTo "
                    href="#inscription"
                  >
                    Lancez votre recherche
                  </a>
                </div>
              </div>
            </div>
          </div>
        </header>
      </section>
    );
  }
}