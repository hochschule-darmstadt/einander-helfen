<!-- The page 'Datenschutzerkärung' containing the data protection declaration of einander-helfen.org.-->

<template>
  <div class="privacy">
    <Header />
    <section class="container pt-6">
      <h1 class="wordbreak">
        {{ $t("privacy.privacyHeadline") }}
      </h1>

      <h2>{{ $t("privacy.dataProtection.dataProtectionHeadline") }}</h2>

      <h3>{{ $t("privacy.dataProtection.generalNotesHeadline") }}</h3>
      <p>
        {{ $t("privacy.dataProtection.generalNotesDiscription1") }}
      </p>
      <h3>{{ $t("privacy.dataProtection.dataCollectionWebsiteHeadline") }}</h3>
      <p class="text-success">
        <strong>{{ $t("privacy.dataProtection.dataCollectionWebsiteQuestion1") }}</strong>
      </p>
      <p>
        {{ $t("privacy.dataProtection.dataCollectionWebsiteAnswer1") }}
      </p>
      <p class="text-success">
        <strong>{{ $t("privacy.dataProtection.dataCollectionWebsiteQuestion2") }}</strong>
      </p>
      <p>
        {{ $t("privacy.dataProtection.dataCollectionWebsiteAnswer2Part1") }}
      </p>
      <p>
        {{ $t("privacy.dataProtection.dataCollectionWebsiteAnswer2Part2") }}
      </p>
      <p class="text-success">
        <strong>{{ $t("privacy.dataProtection.dataCollectionWebsiteQuestion3") }}</strong>
      </p>
      <p>
        {{ $t("privacy.dataProtection.dataCollectionWebsiteAnswer3") }}
      </p>
      <p class="text-success">
        <strong>{{ $t("privacy.dataProtection.dataCollectionWebsiteQuestion4") }}</strong>
      </p>
      <p>
        {{ $t("privacy.dataProtection.dataCollectionWebsiteAnswer4Part1") }}
      </p>
      <p>
        {{ $t("privacy.dataProtection.dataCollectionWebsiteAnswer4Part2") }}
      </p>
      <h2>{{ $t("privacy.mandatoryInformation.mandatoryInformationHeadline") }}</h2>

      <h3>{{ $t("privacy.mandatoryInformation.privacyHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.privacyDescription1") }}
      </p>
      <p>
        {{ $t("privacy.mandatoryInformation.privacyDescription2") }}
      </p>
      <p>
        {{ $t("privacy.mandatoryInformation.privacyDescription3") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.noteResponsibleBodyHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.responsibleBodyDataProcessing") }}
      </p>
      Roland Humm <br />
      Pragelatostr. 113<br />
      D-64372<br />
      Ober Ramstadt <br />
      <p>
        <a href="mailto:info@einander-helfen.org">info@einander-helfen.org</a>
      </p>

      <p>
        {{ $t("privacy.mandatoryInformation.noteResponsibleBodyDescription1") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.revocationConsentDataProcessingHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.revocationConsentDataProcessingDescription1") }}
      </p>

      <h3>
        {{ $t("privacy.mandatoryInformation.rightToObjectDataCollectionHeadline") }} 
      </h3>
      <p>
        <strong>{{ $t("privacy.mandatoryInformation.rightToObjectDataCollectionDescription1") }}</strong>
      </p>
      <p>
        <strong>{{ $t("privacy.mandatoryInformation.rightToObjectDataCollectionDescription2") }}</strong>
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.rightOfComplaintSupervisoryAuthorityHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.rightOfComplaintSupervisoryAuthorityDescription1") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.rightDataPortabilityHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.rightDataPortabilityDescription1") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.informationBlockingDeletionCorrectionHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.informationBlockingDeletionCorrectionDescription1") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.rightRestrictionProcessingHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.rightRestrictionProcessingDescription1") }}
      </p>
      <ul>
        <li>
          {{ $t("privacy.mandatoryInformation.rightRestrictionProcessingDescription1Part1") }}
        </li>
        <li>
          {{ $t("privacy.mandatoryInformation.rightRestrictionProcessingDescription1Part2") }}
        </li>
        <li>
          {{ $t("privacy.mandatoryInformation.rightRestrictionProcessingDescription1Part3") }}
        </li>
        <li>
          {{ $t("privacy.mandatoryInformation.rightRestrictionProcessingDescription1Part4") }}
        </li>
      </ul>
      <p>
        {{ $t("privacy.mandatoryInformation.rightRestrictionProcessingDescription2") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.oppositionAdvertisingMailsHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.oppositionAdvertisingMailsDescription1") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.usageStatisticsHeadline") }}</h3>

      <p>
        {{ $t("privacy.mandatoryInformation.usageStatisticsDescription1Part1") }}
        <a href="https://matomo.org" target="_blank">Matomo</a>, 
        {{ $t("privacy.mandatoryInformation.usageStatisticsDescription1Part2") }}
        <a href="https://matomo.org/faq/new-to-piwik/" target="_blank"
          >https://matomo.org/faq/new-to-piwik/</a
        >
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.serverLogFileHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.serverLogFileDescription1") }}
      </p>
      <ul>
        <li>{{ $t("privacy.mandatoryInformation.serverLogFileDescription1Part1") }}</li>
        <li>{{ $t("privacy.mandatoryInformation.serverLogFileDescription1Part2") }}</li>
        <li>{{ $t("privacy.mandatoryInformation.serverLogFileDescription1Part3") }}</li>
        <li>{{ $t("privacy.mandatoryInformation.serverLogFileDescription1Part4") }}</li>
        <li>{{ $t("privacy.mandatoryInformation.serverLogFileDescription1Part5") }}</li>
        <li>{{ $t("privacy.mandatoryInformation.serverLogFileDescription1Part6") }}</li>
      </ul>
      <p>
        {{ $t("privacy.mandatoryInformation.serverLogFileDescription2") }}
      </p>
      <p>
        {{ $t("privacy.mandatoryInformation.serverLogFileDescription3") }}
      </p>

      <h3>{{ $t("privacy.mandatoryInformation.requestByHeadline") }}</h3>
      <p>
        {{ $t("privacy.mandatoryInformation.requestByDescription1") }}
      </p>
      <p>
        {{ $t("privacy.mandatoryInformation.requestByDescription2") }}
      </p>
      <p>
        {{ $t("privacy.mandatoryInformation.requestByDescription3") }}
      </p>
      <p>{{ $t("privacy.mandatoryInformation.source") }} <a href="https://www.e-recht24.de">e-recht24.de</a></p>
    </section>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/SearchHeader.vue";

export default Vue.extend({
  name: "Privacy",
  components: {
    Header,
  },
});
</script>

<style lang="scss" scoped></style>
