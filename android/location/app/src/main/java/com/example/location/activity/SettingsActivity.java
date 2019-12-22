package com.example.location.activity;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;

import com.example.location.api.system.SystemConfiguration;
import com.example.location.R;

import static com.example.location.api.system.SystemConfigurationBuilder.systemConfigurationBuilder;
import static java.lang.Float.parseFloat;
import static java.lang.Integer.parseInt;

public class SettingsActivity extends AppCompatActivity {

    //SYSTEM CONFIG ATTRIBUTE KEYS
    public static final String MEDIUM_COEF_ATTRIBUTE = "MEDIUM_COEF_SIGNAL_KEY";

    //DEFAULT VALUES
    private static final String DEFAULT_SERVER_IP = "10.42.0.1";
    private static final int DEFAULT_SERVER_PORT = 8082;
    private static final float DEFAULT_MEDIUM_COEF = 4.0f;
    private static final String USER_ID = "USER";

    //SHARED PREFERENCES KEYS
    private static final String SETTINGS_SHARED_PREFERENCES_KEY = "SETTINGS_SHARED_PREFERENCES_KEY";
    private static final String USER_ID_KEY = "user_id";
    private static final String SERVER_IP_KEY = "server_ip";
    private static final String SERVER_PORT_KEY = "server_port";
    private static final String MEDIUM_COEF_KEY = "medium_coef";

    public static SystemConfiguration getSystemConfig(Context context) {
        SharedPreferences sharedPreferences = context.getSharedPreferences(SETTINGS_SHARED_PREFERENCES_KEY, MODE_PRIVATE);

        String userId = sharedPreferences.getString(USER_ID_KEY, USER_ID);
        String serverIp = sharedPreferences.getString(SERVER_IP_KEY, DEFAULT_SERVER_IP);
        int serverPort = sharedPreferences.getInt(SERVER_PORT_KEY, DEFAULT_SERVER_PORT);
        float mediumCoef = sharedPreferences.getFloat(MEDIUM_COEF_KEY, DEFAULT_MEDIUM_COEF);

        return systemConfigurationBuilder()
                .withUserId(userId)
                .withServerIp(serverIp)
                .withServerPort(serverPort)
                .withCustomConfigAttribute(MEDIUM_COEF_ATTRIBUTE, mediumCoef)
                .build();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings_layout);

        EditText configuredIp = findViewById(R.id.ipConfigEditText);
        EditText configuredPort = findViewById(R.id.portConfigEditText);
        EditText configuredMediumCoef = findViewById(R.id.mediumCoefEditText);

        SystemConfiguration systemConfiguration = getSystemConfig(this);

        configuredIp.setText(systemConfiguration.getServerHost());
        configuredPort.setText(Integer.toString(systemConfiguration.getServerPort()));
        configuredMediumCoef.setText(Float.toString(systemConfiguration.getConfigAttribute(MEDIUM_COEF_ATTRIBUTE)));

    }

    public void updateSettings(View view) {
        SharedPreferences.Editor sharedPreferencesEditor = this.getSharedPreferences(SETTINGS_SHARED_PREFERENCES_KEY, MODE_PRIVATE).edit();

        String configuredIp = ((EditText)findViewById(R.id.ipConfigEditText)).getText().toString();
        int configuredPort = parseInt(((EditText)findViewById(R.id.portConfigEditText)).getText().toString());
        float configuredMediumCoef = parseFloat(((EditText)findViewById(R.id.mediumCoefEditText)).getText().toString());

        sharedPreferencesEditor.putString(SERVER_IP_KEY, configuredIp);
        sharedPreferencesEditor.putInt(SERVER_PORT_KEY, configuredPort);
        sharedPreferencesEditor.putFloat(MEDIUM_COEF_KEY, configuredMediumCoef);

        sharedPreferencesEditor.apply();
        finish();
    }

}
