package com.example.GUI;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import android.content.Intent;
import android.content.Context;
import androidx.appcompat.app.AppCompatActivity;
import android.widget.RadioButton;
import androidx.appcompat.app.ActionBar;
import android.view.LayoutInflater;
import androidx.appcompat.widget.Toolbar;

public class RadioActivity extends AppCompatActivity {

	RadioButton radioButton00, radioButton01;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_radio);
		this.getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
		getSupportActionBar().setDisplayShowCustomEnabled(true);
		LayoutInflater inflator=   (LayoutInflater)this.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		View v=inflator.inflate(R.layout.action_bar_radio, null);
		ActionBar.LayoutParams layoutParams = new ActionBar.LayoutParams(ActionBar.LayoutParams.MATCH_PARENT,ActionBar.LayoutParams.MATCH_PARENT);
		getSupportActionBar().setCustomView(v, layoutParams);
		Toolbar parent = (Toolbar) v.getParent();
		parent.setContentInsetsAbsolute(0, 0);
		radioButton00 = (RadioButton)findViewById(R.id.RadioButton_0_5_0);
		radioButton01 = (RadioButton)findViewById(R.id.RadioButton_0_6_0);
		radioButton00.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				radioButton00.setChecked(true);
				radioButton01.setChecked(false);
			}
		});		radioButton01.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				radioButton01.setChecked(true);
				radioButton00.setChecked(false);
			}
		});	}
	public void clickMe0_0_0(View view){
	// onClick logic_0_0_0
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_0_2(View view){
	// onClick logic_0_0_2
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_0_3(View view){
	// onClick logic_0_0_3
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
}