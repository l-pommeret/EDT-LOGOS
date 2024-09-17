import React from "react";
import license from "../../LICENCE.txt";
import p from "../../package.json";

export default function Help() {
  return (
    <>
      <h1><code>ical-ufr</code> {p["version"]} &ndash; À Propos</h1>

      <h2>Description</h2>
      <p>Ces pages présentent les emplois du temps des formations liées à l&rsquo;UFR de mathématiques, sur la base de réservations de salles qui les concernent effectuées sur la plate-forme ADE.</p>

      <h3>Affichage d&rsquo;un emploi du temps</h3>
      <ul>
        <li>Sélectionner le parcours et l&rsquo;année à l&rsquo;aide des onglets.</li>
        <li>Restreindre l&rsquo;affichage au groupe d&rsquo;étudiants concerné.</li>
        <li>Activer la case « obsolète » pour afficher les réservations récemment supprimées.</li>
      </ul>

      <p>Vous pouvez cliquer sur une réservation pour en afficher les détails. Pour la refermer, cliquez sur le bouton en forme de croix, en-dehors des détails, ou appuyez sur la touche <code>échap</code>.</p>

      <h3>Liens permanents</h3>
      <p>Les liens au bas du calendrier permettent de télécharger les données ADE au format ical, ou d&rsquo;obtenir le lien vers l&rsquo;affichage de l&rsquo;emploi du temps d&rsquo;un groupe donné.</p>

      <h3><a href="review/archive23-24/#">Archives 2023-24 et antérieures</a></h3>
        <p>Suite au trop grand nombre de modifications dans les numeros de fiches en 2024-25, merci d&rsquo;utiliser le lien ci dessus pour obtenir les annees antérieures.</p>
      <h3>Date par défaut</h3>
      <p>Il est possible de passer un paramètre d&rsquo;archive pour une autre année et un paramètre de date. Attention à bien le placer avant le #.
        <li> <a href="?archive=2022-23">2022-23</a>, <a href="?archive=2021-22">2021-22</a></li>
        <li> Exemple d&rsquo;archive et date: <a href="?archive=2021-22&date=2022-02-05#/parcours/miashs/l2">?archive=2021-22&date=2022-02-05#/parcours/miashs/l2</a></li>
        <li> Exemple de date pour l&rsquo;annee courante: <a href="?date=2021-09-15#/parcours/miashs/l2">?date=2021-09-15#/parcours/miashs/l2</a></li>
        <li> Exemple de préselection de quelques groupes seulement: <a href="#/parcours/miashs/l2/6599+6600">#/parcours/miashs/l2/6599+6600</a></li>
      </p>
      <h3>Remarques</h3>
      <ul>
        <li><p>Une activité ne faisant pas l&rsquo;objet de réservation sur la plate-forme ADE ne peut pas être incluse dans l&rsquo;affichage.</p></li>
        <li><p>Les données de réservations concernant chaque groupe d&rsquo;étudiant sont préchargées chaque nuit. Les réservations du jour n&rsquo;apparaissent donc pas.</p></li>
      </ul>

      <h2>Option manuelle (enseignants)</h2>
      <p>Il est possible de choisir manuellement la liste des groupes à afficher (potentiellement d&rsquo;années et parcours différents) en se rendant à l&rsquo;adresse <a href="#/manuel">/manuel</a>.</p>

      <h2>En cas de problème</h2>
      <p>Merci d&rsquo; écrire à l&rsquo; adresse <a href="mailto:gitlab+molin-ical-ufr-734-issue-@math.univ-paris-diderot.fr"><code>gitlab+molin-ical-ufr-734-issue-@math.univ-paris-diderot.fr</code></a> en cas de problème technique avec l&rsquo; application web. <strong>Pas en cas de problème avec vos emplois du temps, des questions générales sur votre formation, de demandes de réservations...</strong></p>

      <h2>Code source</h2>
      <p>Le projet est open-source et adaptable aux besoin d&rsquo;autres UFR ou d&rsquo;autres utilisateurs du logiciel ADE : <a href="https://gitlab.math.univ-paris-diderot.fr/molin/ical-ufr">https://gitlab.math.univ-paris-diderot.fr/molin/ical-ufr</a></p>

      <h2>Licence</h2>
      <pre>
        <code>
          {license}
        </code>
      </pre>
    </>
  );
}
