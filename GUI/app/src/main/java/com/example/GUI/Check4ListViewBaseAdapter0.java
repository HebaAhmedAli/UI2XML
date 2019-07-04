package com.example.GUI;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import java.util.ArrayList;
import java.util.List;
import android.widget.TextView;
public class Check4ListViewBaseAdapter0 extends BaseAdapter {
	public ArrayList<Check4ListViewBean0> arrayListListener;
	private List<Check4ListViewBean0> mListenerList;
	Context mContext;
	public Check4ListViewBaseAdapter0(List<Check4ListViewBean0> mListenerList, Context context) {
		mContext = context;
		this.mListenerList = mListenerList;
		this.arrayListListener = new ArrayList<Check4ListViewBean0>();
		this.arrayListListener.addAll(mListenerList);
	}
	public class ViewHolder {
		TextView textView0;
	}
	@Override
	public int getCount() {
		return mListenerList.size();
	}
	@Override
	public Object getItem(int position) {
		return mListenerList.get(position);
	}
	@Override
	public long getItemId(int position) {
		return position;
	}
	@Override
	public View getView(final int position, View view, ViewGroup parent) {
		final ViewHolder holder;
		if (view == null) {
			view = LayoutInflater.from(mContext).inflate(R.layout.list_view0_0_2, null);
			holder = new ViewHolder();
			holder.textView0 = (TextView) view.findViewById(R.id.TextView_0_2_1);
			view.setTag(holder);
		}
		else {
			holder = (ViewHolder) view.getTag();
		}
		try {
			holder.textView0.setText(mListenerList.get(position).getText0());
		} catch (Exception ex){
		}
		return view;
	}
}