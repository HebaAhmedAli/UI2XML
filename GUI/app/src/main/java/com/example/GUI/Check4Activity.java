package com.example.GUI;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import android.content.Intent;
import android.content.Context;
import androidx.appcompat.app.AppCompatActivity;
import android.widget.RadioButton;

public class Check4Activity extends AppCompatActivity {

	RadioButton radioButton00, radioButton01;
	RadioButton radioButton10, radioButton11;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_check4);
		radioButton00 = (RadioButton)findViewById(R.id.RadioButton_0_0_0);
		radioButton01 = (RadioButton)findViewById(R.id.RadioButton_0_0_2);
		radioButton00.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				radioButton00.setChecked(true);
				radioButton01.setChecked(false);
			}
		});
		radioButton01.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				radioButton01.setChecked(true);
				radioButton00.setChecked(false);
			}
		});
		radioButton10 = (RadioButton)findViewById(R.id.RadioButton_0_1_0);
		radioButton11 = (RadioButton)findViewById(R.id.RadioButton_0_1_2);
		radioButton10.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				radioButton10.setChecked(true);
				radioButton11.setChecked(false);
			}
		});
		radioButton11.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				radioButton11.setChecked(true);
				radioButton10.setChecked(false);
			}
		});
	}
}