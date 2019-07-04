package com.example.GUI;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import android.content.Intent;
import android.content.Context;
import androidx.appcompat.app.AppCompatActivity;
import android.widget.ListView;
import java.util.ArrayList;
import android.widget.RadioButton;

public class Check4Activity extends AppCompatActivity {

	ListView lv0;
	Check4ListViewBaseAdapter0 adapter0;
	ArrayList<Check4ListViewBean0> arr_bean0;
	RadioButton radioButton00, radioButton01;
	RadioButton radioButton10, radioButton11;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_check4);
		lv0 = (ListView) findViewById(R.id.ListView0_0_2);
		arr_bean0=new ArrayList<>();
		arr_bean0.add(new Check4ListViewBean0("Heba"));
		arr_bean0.add(new Check4ListViewBean0("Figyel"));
		arr_bean0.add(new Check4ListViewBean0("Fatema"));
		arr_bean0.add(new Check4ListViewBean0("Sobhy"));
		adapter0=new Check4ListViewBaseAdapter0(arr_bean0,this);
		lv0.setAdapter(adapter0);
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