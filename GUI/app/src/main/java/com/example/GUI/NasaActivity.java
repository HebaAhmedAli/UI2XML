package com.example.GUI;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import android.content.Intent;
import android.content.Context;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.ActionBar;
import android.view.LayoutInflater;
import androidx.appcompat.widget.Toolbar;

public class NasaActivity extends AppCompatActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_nasa);
		this.getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
		getSupportActionBar().setDisplayShowCustomEnabled(true);
		LayoutInflater inflator=   (LayoutInflater)this.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		View v=inflator.inflate(R.layout.action_bar_nasa, null);
		ActionBar.LayoutParams layoutParams = new ActionBar.LayoutParams(ActionBar.LayoutParams.MATCH_PARENT,ActionBar.LayoutParams.MATCH_PARENT);
		getSupportActionBar().setCustomView(v, layoutParams);
		Toolbar parent = (Toolbar) v.getParent();
		parent.setContentInsetsAbsolute(0, 0);
	}
	public void clickMe0_0_0(View view){
	// onClick logic_0_0_0
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_1_0(View view){
		Intent intent = new Intent(NasaActivity.this, MainActivity.class);
		startActivity(intent);
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_2_0(View view){
	// onClick logic_0_2_0
		Toast.makeText(getApplicationContext(),"Clicked on Button",Toast.LENGTH_SHORT).show();
	}
}