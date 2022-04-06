The Automatic Translation service can easily be extended to support for example DeepL and Microsoft Translate in the future. A short experiment has already been done with both translation providers, as can be seen in this code:


```kotlin
import com.google.gson.Gson
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request

// DeepL Translator documentation:
// - https://www.deepl.com/pro-api
// - https://www.deepl.com/docs-api
// - https://www.deepl.com/docs-api/translating-text/request/
// - https://support.deepl.com/hc/en-us/articles/360019925219-Languages-included-in-DeepL-Pro


@Suppress("SpellCheckingInspection")
private val text = "Im achzehnten Jahrhundert lebte in Frankreich ein Mann, der zu den genialsten und " +
        "abscheulichsten Gestalten dieser an genialen und abscheulichen Gestalten nicht armen Epoche gehörte."


fun main() {
//    TryDeepLTranslator().tryTranslator(text, "EN-US")
//    TryDeepLTranslator().tryTranslator(text, "NL")
    TryDeepLTranslator().tryTranslator(text, "ZH")
}


class TryDeepLTranslator {
    // todo: The DeepL Translator configuration consists of the authentication key.

    private val authenticationKey = "Add your authentication key here..."

    private val configurationJson = "{\"authenticationKey\":\"$authenticationKey\"}"
    private val configuration = Gson().fromJson(configurationJson, DeepLTranslatorConfiguration::class.java)

    fun tryTranslator(text: String, destinationLanguage: String) {
        val client = OkHttpClient()

        val formBody = FormBody.Builder()
            .add("auth_key", configuration.authenticationKey)
            .add("text", text)
            .add("target_lang", destinationLanguage)
            .build()

        val request = Request.Builder()
            .url("https://api-free.deepl.com/v2/translate")
            .post(formBody)
            .build()

        client.newCall(request).execute().use { response ->
            if (response.isSuccessful) {
                val translationResponse = response.body?.string()
                println("translationResponse: $translationResponse")
                println()
                val translationResults = Gson().fromJson(translationResponse, DeepLTranslationResults::class.java)
                println("Translation results:")
                println(translationResults)
            } else {
                println("Unexpected code: $response.")
            }
        }
    }
}


data class DeepLTranslatorConfiguration(val authenticationKey: String)

data class DeepLTranslationResults(val translations: List<DeepLTranslation>)
data class DeepLTranslation(val detected_source_language: String, val text: String)
```


```kotlin
import com.google.gson.Gson
import okhttp3.HttpUrl
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody


// Microsoft Translator documentation:
// - https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?tabs=java
// - https://www.microsoft.com/en-us/translator/business/machine-translation/


fun main() {
    TryMicrosoftTranslator().tryTranslator("Hello World!", listOf("de", "it", "nl"))
}


class TryMicrosoftTranslator {
    // todo: The Microsoft Translator configuration consists of the subscription key and the location/region.

    // If the region is incorrect, the following error is returned:
    // {"error":{"code":401000,"message":"The request is not authorized because credentials are missing or invalid."}}

    private val subscriptionKey = "Add your subscription key here..."

    // Specify the region (also known as location) you used when creating the Translator resource in Azure. The region
    // is case-insensitive, and you have to remove the spaces. For example, for West Europe you can use "WestEurope".
    private val region = "WestEurope"
//    private val region = "global"

    private val configurationJson = "{\"subscriptionKey\":\"$subscriptionKey\",\"region\":\"$region\"}"
    private val configuration = Gson().fromJson(configurationJson, MicrosoftTranslatorConfiguration::class.java)

    fun tryTranslator(text: String, destinationLanguages: List<String>) {
        val translationResponse = translate(text, destinationLanguages)
        println("translationResponse: $translationResponse")
        println()
        val translationResults = Gson().fromJson(translationResponse, Array<MicrosoftTranslationResults>::class.java)
        println("Translation results:")
        println(translationResults[0])
    }

    @Suppress("SameParameterValue")
    private fun translate(text: String, destinationLanguages: List<String>): String {
        val body = "[{\"Text\": \"$text\"}]".toRequestBody("application/json".toMediaTypeOrNull())

        val request = Request.Builder()
            .url(createUrl(destinationLanguages))
            .post(body)
            .addHeader("Ocp-Apim-Subscription-Key", configuration.subscriptionKey)
            .addHeader("Ocp-Apim-Subscription-Region", configuration.region)
            .addHeader("Content-type", "application/json")
            .build()

        val response = OkHttpClient().newCall(request).execute()

        return response.body?.string() ?: ""
    }

    private fun createUrl(destinationLanguages: List<String>): HttpUrl {
        var urlInProgress = HttpUrl.Builder()
            .scheme("https")
            .host("api.cognitive.microsofttranslator.com")
            .addPathSegment("/translate")
            .addQueryParameter("api-version", "3.0")

        destinationLanguages.forEach { language ->
            urlInProgress = urlInProgress.addQueryParameter("to", language)
        }

        return urlInProgress.build()
    }
}


data class MicrosoftTranslatorConfiguration(val subscriptionKey: String, val region: String)

data class MicrosoftTranslationResults(val detectedLanguage: MicrosoftDetectedLanguage,
                                       val translations: List<MicrosoftTranslation>)
data class MicrosoftDetectedLanguage(val language: String, val score: Double)
data class MicrosoftTranslation(val text: String, val to: String)
```


```kotlin
// File: build.gradle.kts

plugins {
    kotlin("jvm") version "1.6.10"
    java
}

group = "com.topdesk.automatic.translation"
version = "0.0.6-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
    implementation("com.squareup.okhttp3:okhttp:4.9.3")
    implementation("com.google.code.gson:gson:2.8.9")
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.8.2")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.8.2")
}

tasks.getByName<Test>("test") {
    useJUnitPlatform()
}
```
